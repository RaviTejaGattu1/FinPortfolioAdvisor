📈 Stock Portfolio Suggestion Engine
A web-based Python application that suggests stock/ETF portfolios based on user-selected investment strategies and investment amounts.

🌐 Live Demo

🔧 Features
User Input

Investment amount (minimum $5000 USD)

Choose 1–2 strategies:

Ethical

Growth

Index

Quality

Value

App Output

Descriptions of selected strategies

Suggested stocks/ETFs with allocated shares and dollar amounts

Real-time portfolio value using yFinance

Interactive 5-day trend chart of portfolio performance

Error Handling

Invalid investment amounts

Incorrect or missing strategy selections

API failures

No internet connection

Deployment

Publicly accessible via Render

⚙️ Local Development Setup
Clone the repository

bash
Copy
Edit
git clone https://github.com/your-username/stock-portfolio-engine.git
cd stock-portfolio-engine
Create and activate virtual environment

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run the application

bash
Copy
Edit
python3 app.py
Access the app locally
Open http://127.0.0.1:5000 in your browser.

🚀 Deployment
Hosted on: 

Configuration

Build command:

bash
Copy
Edit
pip install -r requirements.txt
Start command:

bash
Copy
Edit
gunicorn app:app
Live URL: (Add once deployed)

🧪 Example Output
Input:

Investment: $10,000

Strategy: Index Investing

Result:

Strategy Description:
Index Investing: Tracks broad market indices...

Allocation:

VTI: 30 shares @ $250.00 → $7,500.00

IXUS: 20 shares @ $60.00 → $1,200.00

ILTB: 10 shares @ $50.00 → $500.00

Current Value: $9,200.00

Trend: Interactive 5-day chart of daily closing prices

📋 Requirements
Python 3.8+

Libraries:

flask

yfinance

pandas

plotly

gunicorn

(See requirements.txt for full list.)

📝 Notes
Uses yFinance for real-time and historical stock/ETF data — no API key required.

Portfolio allocates funds evenly across selected securities using whole shares.

Trend chart displays adjusted close values for the past 5 trading days.
