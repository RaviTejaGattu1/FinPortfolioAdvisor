#703138cf3a9234b03857070384d7153cb7b21b05
import os
from flask import Flask, request, render_template
from tiingo import TiingoClient
from datetime import datetime, timedelta
import socket
import pandas as pd
import plotly.express as px
import plotly.io as pio
import logging
import time
import random
import pickle
import os.path

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Tiingo client
tiingo_client = TiingoClient({"api_key": "703138cf3a9234b03857070384d7153cb7b21b05"})  # Replace with your API key

# Cache file
CACHE_FILE = "tiingo_cache.pkl"
CACHE_DURATION = 3600  # Cache for 1 hour

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

def load_cache():
    """Load cached Tiingo data if available and not expired."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rb') as f:
            cache = pickle.load(f)
            if time.time() - cache.get('timestamp', 0) < CACHE_DURATION:
                app.logger.debug("Loaded valid cache")
                return cache.get('data', {})
    return {}

def save_cache(data):
    """Save Tiingo data to cache."""
    cache = {'timestamp': time.time(), 'data': data}
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(cache, f)
    app.logger.debug("Saved data to cache")

def get_stock_data(symbol, retries=3, backoff_factor=1):
    """Fetch current price and 5-day historical data using Tiingo with retry logic."""
    # Check cache
    cache = load_cache()
    if symbol in cache:
        app.logger.debug(f"Using cached data for {symbol}")
        return cache[symbol], None

    for attempt in range(retries):
        try:
            app.logger.debug(f"Fetching data for {symbol}, attempt {attempt + 1}")
            # Get current quote
            quote = tiingo_client.get_ticker_price(ticker=symbol, fmt='json')
            if not quote or not isinstance(quote, list) or len(quote) == 0 or 'close' not in quote[0]:
                app.logger.error(f"Invalid quote response for {symbol}: {quote}")
                return None, f"Error: Invalid symbol '{symbol}'."
            
            current_price = float(quote[0]['close'])
            
            # Get 5-day historical data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=10)  # Buffer for trading days
            history = tiingo_client.get_dataframe(tickers=symbol, startDate=start_date.strftime("%Y-%m-%d"), endDate=end_date.strftime("%Y-%m-%d"), frequency='daily')
            if history.empty:
                app.logger.error(f"No historical data for {symbol}")
                return None, f"Error: No historical data for '{symbol}'."
            
            # Extract last 5 trading days
            available_days = min(len(history), 5)
            dates = history.index[-available_days:].strftime("%Y-%m-%d").tolist()
            closes = history['close'][-available_days:].tolist()
            history_dict = dict(zip(dates, closes))
            
            # Set previous_close from the second-to-last day’s close
            previous_close = float(history['close'][-2]) if len(history) >= 2 else current_price
            
            # Cache data
            data = {"current_price": current_price, "previous_close": previous_close, "history": history_dict}
            cache[symbol] = data
            save_cache(cache)
            
            app.logger.debug(f"Data fetched for {symbol}: price={current_price}, previous_close={previous_close}, history={history_dict}")
            return data, None
        except Exception as e:
            app.logger.error(f"Error fetching data for {symbol} on attempt {attempt + 1}: {str(e)}")
            if attempt < retries - 1:
                sleep_time = backoff_factor * (2 ** attempt) + random.uniform(0, 0.1)
                app.logger.debug(f"Retrying after {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
            else:
                return None, f"Error: Unable to fetch data for '{symbol}'. Details: {str(e)}"
        time.sleep(2)  # 500 requests/hour = ~2s delay

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
        if not data["history"]:
            app.logger.error(f"Empty historical data for {symbol}")
            return None, f"Error: No historical data available for '{symbol}'."
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
            amount_str = request.form.get("amount")
            if not amount_str:
                app.logger.error("No amount provided")
                return render_template("index.html", error="Please enter a dollar amount.", strategies=STRATEGY_MAPPINGS.keys())
            amount = float(amount_str)
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
        except ValueError as e:
            app.logger.error(f"Invalid amount entered: {str(e)}")
            return render_template("index.html", error="Please enter a valid dollar amount.", strategies=STRATEGY_MAPPINGS.keys())
        except Exception as e:
            app.logger.error(f"Unexpected error: {str(e)}")
            return render_template("index.html", error=f"An unexpected error occurred: {str(e)}", strategies=STRATEGY_MAPPINGS.keys())
    
    return render_template("index.html", strategies=STRATEGY_MAPPINGS.keys())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)