# 📈 Stock Portfolio Suggestion Engine

A web-based Python application that suggests stock/ETF portfolios based on user-selected investment strategies and investment amounts.  

---


## 🌐 Live Demo
Live Application Deployed URL : 


Strategy : Ethical

https://github.com/user-attachments/assets/3a9511cc-1dfe-4a87-8226-2daf2201eaea

Strategy : Quality

https://github.com/user-attachments/assets/ab723303-968a-4f8a-8155-f24acc0e1de2

<img width="1256" alt="image" src="https://github.com/user-attachments/assets/111801e8-e2c7-4cf3-b104-148610287f56" />

<img width="1171" alt="image" src="https://github.com/user-attachments/assets/91daf538-0e54-4c4b-98ad-c1cd965ad376" />

**URL:** 

---

## 🔧 Features

- **User Input:**
  - Investment amount (minimum **$5000 USD**)
  - Choose 1–2 strategies:
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
  - `yfinance`
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
