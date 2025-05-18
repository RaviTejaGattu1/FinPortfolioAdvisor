# 📈 Stock Portfolio Suggestion Engine

A web-based Python application that suggests stock/ETF portfolios based on user-selected investment strategies and investment amounts.  

---


## 🌐 Live Demo


Strategy : Ethical

https://github.com/user-attachments/assets/3a9511cc-1dfe-4a87-8226-2daf2201eaea

Strategy : Quality

https://github.com/user-attachments/assets/ab723303-968a-4f8a-8155-f24acc0e1de2

<img width="1256" alt="image" src="https://github.com/user-attachments/assets/111801e8-e2c7-4cf3-b104-148610287f56" />

<img width="1171" alt="image" src="https://github.com/user-attachments/assets/91daf538-0e54-4c4b-98ad-c1cd965ad376" />

**URL:** https://portfolioadvisor.onrender.com/

---

## Features

- **Investment Strategies**: Choose from five strategies (Ethical, Growth, Index, Quality, Value) via radio buttons for single selection.
- **Portfolio Allocation**: Displays number of shares, allocated value, value change, and percentage change for each security.
- **5-Day Trend Chart**: Visualizes portfolio value over the last five trading days using Plotly with a gold-themed design.
- **Premium UI**: Built with Tailwind CSS, featuring a green/gold gradient for a professional look.
- **Real-Time Data**: Fetches stock prices and historical data using the Tiingo API (50,000 requests/month, 500/hour).
- **Error Handling**: Validates inputs (minimum $5,000) and handles API errors gracefully.
- **Caching**: Stores API responses in `tiingo_cache.pkl` for 1 hour to optimize performance.
- **Deployment**: Hosted on Render for reliable access.

## Tech Stack

- **Backend**: Python 3.10, Flask 2.3.3
- **API**: Tiingo (replaced Polygon.io, Alpha Vantage, yfinance, IEX Cloud due to rate limits and obsolescence)
- **Frontend**: HTML, Tailwind CSS 2.2.19
- **Data Processing**: Pandas 2.2.2, Plotly 5.22.0
- **Deployment**: Render, Gunicorn 23.0.0
- **Version Control**: Git, GitHub

## Investment Strategies and Securities

| Strategy | Description | Example Securities |
|----------|-------------|------------|
| Ethical | Focuses on ESG practices | AAPL, ADBE, NSRGY |
| Growth | Targets high-growth companies | NVDA, TSLA, AMZN |
| Index | Tracks broad market indices | VTI, IXUS, ILTB |
| Quality | Selects financially stable firms | MSFT, JNJ, PG |
| Value | Targets undervalued stocks | BRK-B, INTC, JPM |

- ## 🔧 Features

- **User Input:**
  - Investment amount (minimum **$5000 USD**)
  - Choose 1strategies:
    - Ethical
    - Growth
    - Index
    - Quality
    - Value

- **App Output:**
  - Descriptions of selected strategies
  - Suggested stocks/ETFs with allocated **shares and dollar amounts**
  - **Real-time** portfolio value using **yFinance**
  - **Interactive 5-day trend chart** of portfolio performance

- **Robust Error Handling:**
  - Invalid investment amounts
  - Missing/invalid strategy selections
  - API failures
  - Internet connectivity issues

- **Deployment:**
  - Publicly accessible via **Render**

---

## ⚙️ Local Development Setup

1. **Clone the Repository**

    ```bash
    git clone https://github.com/your-username/stock-portfolio-engine.git
    cd stock-portfolio-engine
    ```

2. **Create and Activate a Virtual Environment**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application**

    ```bash
    python3 app.py
    ```

5. **Access the App**

    Open your browser and go to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🚀 Deployment

- **Platform:** [Render](https://render.com)

- **Configuration:**
    - **Build command:**

        ```bash
        pip install -r requirements.txt
        ```

    - **Start command:**

        ```bash
        gunicorn app:app
        ```

- **Live URL:** *(Add once deployed)*

---

## 🧪 Example Output

**Input:**
- Investment: `$10,000`
- Strategy: `Index Investing`

**Output:**

- **Strategy Description:**
    > Index Investing: Tracks broad market indices...

- **Allocation:**
    - `VTI`: 30 shares @ $250.00 → **$7,500.00**
    - `IXUS`: 20 shares @ $60.00 → **$1,200.00**
    - `ILTB`: 10 shares @ $50.00 → **$500.00**

- **Current Value:** `$9,200.00`
- **Trend:** Interactive 5-day chart (adjusted close values)

---

## 📋 Requirements

- **Python** 3.8+
- **Libraries:**
  - `flask`
  - `pandas`
  - `plotly`
  - `gunicorn`

> See `requirements.txt` for the complete list.

---

## 📝 Notes

- Uses **yFinance** for fetching real-time and historical stock/ETF data (no API key required).
- Portfolio allocation is split **evenly across selected securities**, using **whole shares** only.
- Trend chart displays **adjusted closing prices** from the **last 5 trading days**.

---
