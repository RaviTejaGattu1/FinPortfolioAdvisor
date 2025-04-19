import os
from flask import Flask, request, render_template
import yfinance as yf
from datetime import datetime, timedelta
from dateutil import tz
import socket
import pandas as pd
import plotly.express as px
import plotly.io as pio
import logging
import time
import random

app = Flask(__name__)

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Investment strategy mappings
STRATEGY_MAPPINGS = {
    "ethical": {
        "description": "Ethical Investing focuses on companies with strong environmental, social, and governance (ESG) practices, promoting sustainability and ethical operations.",
        "securities": ["AAPL", "ADBE", "NSRGY"]
    },
    "growth": {
        "description": "Growth Investing targets companies with high growth potential, typically in technology or innovative sectors, with strong revenue and earnings growth.",
        "securities": ["NVDA", "TSLA", "AMZN"]
    },
    "index": {
        "description": "Index Investing tracks broad market indices for diversified, low-cost exposure to equities or bonds, aiming for steady long-term returns.",
        "securities": ["VTI", "IXUS", "ILTB"]
    },
    "quality": {
        "description": "Quality Investing selects financially stable companies with high return on equity, low debt, and consistent earnings for reliable performance.",
        "securities": ["MSFT", "JNJ", "PG"]
    },
    "value": {
        "description": "Value Investing targets undervalued stocks with low price-to-earnings or price-to-book ratios, expected to appreciate over time.",
        "securities": ["BRK-B", "INTC", "JPM"]
    }
}

def check_internet():
    """Check if there is an internet connection."""
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False

def get_stock_data(symbol, retries=3, backoff_factor=1):
    """Fetch current price and 5-day historical data using yfinance with retry logic."""
    for attempt in range(retries):
        try:
            app.logger.debug(f"Fetching data for {symbol}, attempt {attempt + 1}")
            ticker = yf.Ticker(symbol)
            # Get current price
            quote = ticker.info
            if not quote or "currentPrice" not in quote:
                # Try with exchange suffix
                alt_symbol = f"{symbol}.NYSE"
                app.logger.debug(f"Retrying with {alt_symbol}")
                ticker = yf.Ticker(alt_symbol)
                quote = ticker.info
                if not quote or "currentPrice" not in quote:
                    app.logger.error(f"Invalid quote response for {symbol}: {quote}")
                    return None, f"Error: Invalid symbol '{symbol}'."
            
            current_price = float(quote["currentPrice"])
            previous_close = float(quote["previousClose"])
            
            # Get historical data (10 days to ensure 5 trading days)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=10)
            history = ticker.history(start=start_date, end=end_date, interval="1d")
            
            if history.empty:
                app.logger.error(f"No historical data for {symbol}")
                return None, f"Error: No historical data for '{symbol}'."
            
            # Use available data (at least 1 day, ideally 5)
            available_days = min(len(history), 5)
            dates = history.index[-available_days:].strftime("%Y-%m-%d").tolist()
            closes = history["Close"][-available_days:].tolist()
            history_dict = dict(zip(dates, closes))
            
            app.logger.debug(f"Data fetched for {symbol}: price={current_price}, history={history_dict}")
            return {"current_price": current_price, "previous_close": previous_close, "history": history_dict}, None
        except Exception as e:
            app.logger.error(f"Error fetching data for {symbol} on attempt {attempt + 1}: {str(e)}")
            if attempt < retries - 1:
                sleep_time = backoff_factor * (2 ** attempt) + random.uniform(0, 0.1)
                app.logger.debug(f"Retrying after {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
            else:
                return None, f"Error: Unable to fetch data for '{symbol}'. Details: {str(e)}"

def allocate_portfolio(amount, strategy):
    """Allocate funds to securities based on selected strategy."""
    if amount < 5000:
        return None, "Error: Investment amount must be at least $5000 USD."
    
    if not strategy or strategy not in STRATEGY_MAPPINGS:
        app.logger.error(f"Invalid strategy: {strategy}")
        return None, "Error: Invalid or no strategy selected."
    
    securities = STRATEGY_MAPPINGS[strategy]["securities"]
    app.logger.debug(f"Processing securities for strategy {strategy}: {securities}")
    
    # Fetch current prices and historical data
    portfolio = []
    for symbol in securities:
        data, error = get_stock_data(symbol)
        if error:
            return None, error
        portfolio.append({"symbol": symbol, "current_price": data["current_price"], "previous_close": data["previous_close"], "history": data["history"]})
    
    # Allocate funds equally
    amount_per_security = amount / len(securities)
    allocations = []
    current_value = 0
    historical_values = []
    
    for sec in portfolio:
        shares = amount_per_security // sec["current_price"]  # Whole shares
        allocated_amount = shares * sec["current_price"]
        current_value += allocated_amount
        
        # Calculate historical portfolio values
        sec_history = {date: shares * price for date, price in sec["history"].items()}
        allocations.append({
            "symbol": sec["symbol"],
            "shares": shares,
            "allocated_amount": allocated_amount,
            "current_price": sec["current_price"],
            "value_change": (sec["current_price"] - sec["previous_close"]) * shares,
            "percentage_change": ((sec["current_price"] - sec["previous_close"]) / sec["previous_close"] * 100) if sec["previous_close"] != 0 else 0
        })
        
        # Aggregate historical values
        if not historical_values:
            historical_values = sec_history
        else:
            for date in historical_values:
                if date in sec_history:
                    historical_values[date] += sec_history[date]
    
    # Prepare trend chart
    trend_df = pd.DataFrame([
        {"Date": date, "Portfolio Value": value}
        for date, value in sorted(historical_values.items())
    ])
    fig = px.line(trend_df, x="Date", y="Portfolio Value", title="Portfolio Value Trend (Last 5 Days)")
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Value (USD)",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#ffffff",
        title_font_color="#ffd700"
    )
    trend_chart = pio.to_html(fig, full_html=False)
    
    return {
        "strategy": strategy,
        "description": STRATEGY_MAPPINGS[strategy]["description"],
        "allocations": allocations,
        "current_value": current_value,
        "trend_chart": trend_chart
    }, None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            amount = float(request.form.get("amount"))
            strategy = request.form.get("strategy")
            
            app.logger.debug(f"Received form data: amount={amount}, strategy={strategy}")
            
            if not strategy or strategy not in STRATEGY_MAPPINGS:
                app.logger.error("No valid strategy selected")
                return render_template("index.html", error="Please select one investment strategy.", strategies=STRATEGY_MAPPINGS.keys())
            
            result, error = allocate_portfolio(amount, strategy)
            if error:
                app.logger.error(f"Portfolio allocation error: {error}")
                return render_template("index.html", error=error, strategies=STRATEGY_MAPPINGS.keys())
            
            return render_template("result.html", result=result)
        except ValueError:
            app.logger.error("Invalid amount entered")
            return render_template("index.html", error="Please enter a valid dollar amount.", strategies=STRATEGY_MAPPINGS.keys())
    
    return render_template("index.html", strategies=STRATEGY_MAPPINGS.keys())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)