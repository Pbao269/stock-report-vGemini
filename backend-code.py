import os
import json
import pandas as pd
import yfinance as yf
import google.generativeai as genai
import re
import time
from datetime import datetime, timedelta

# Load ticker mappings from JSON
with open("ticker.json", "r") as f:
    raw_company_data = json.load(f)

def normalize_title(name):
    name = name.lower()
    name = re.sub(r'[^a-z0-9\s]', '', name)
    name = re.sub(r'\b(inc|corp|co|ltd|plc|sa|nv|se|llc|lp|group|holdings|international|limited|technologies|solutions|systems|enterprises?)\b', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

name_to_ticker = {}
# Convert the numbered indices to a ticker-based mapping
for item in raw_company_data.values():
    title = normalize_title(item['title'])
    ticker = item['ticker'].upper()
    name_to_ticker[title] = ticker
    name_to_ticker[ticker] = ticker

# Setup Gemini
genai.configure(api_key="AIzaSyA7YdCpR_0AIerXm7L0p-lte9YRTNcSz10")
model = genai.GenerativeModel("gemini-2.0-flash")

def get_ticker_from_name(input_text):
    input_text_norm = normalize_title(input_text)
    ticker = name_to_ticker.get(input_text.upper()) or name_to_ticker.get(input_text_norm)
    if not ticker:
        raise ValueError(f"Could not find ticker for input: '{input_text}'. Please try a valid company name or ticker.")
    return ticker

def get_stock_data_with_retry(ticker, period='1y', max_retries=3):
    for attempt in range(max_retries):
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            if not hist.empty:
                return hist
            time.sleep(1)  # Wait 1 second before retrying
        except Exception as e:
            if attempt == max_retries - 1:
                raise Exception(f"Failed to fetch data for {ticker} after {max_retries} attempts: {str(e)}")
            time.sleep(1)
    raise Exception(f"No data available for {ticker}")

def get_stock_price(ticker):
    hist = get_stock_data_with_retry(ticker)
    if hist.empty:
        raise ValueError(f"No price data available for {ticker}")
    return hist.iloc[-1].Close

def calculate_SMA(ticker, window):
    hist = get_stock_data_with_retry(ticker)
    return hist.Close.rolling(window=window).mean().iloc[-1]

def calculate_EMA(ticker, window):
    hist = get_stock_data_with_retry(ticker)
    return hist.Close.ewm(span=window, adjust=False).mean().iloc[-1]

def calculate_RSI(ticker):
    hist = get_stock_data_with_retry(ticker)
    close = hist.Close
    delta = close.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=14-1, adjust=False).mean()
    ema_down = down.ewm(com=14-1, adjust=False).mean()
    rs = ema_up / ema_down
    return 100 - (100 / (1 + rs)).iloc[-1]

def calculate_MACD(ticker):
    hist = get_stock_data_with_retry(ticker)
    close = hist.Close
    short_ema = close.ewm(span=12, adjust=False).mean()
    long_ema = close.ewm(span=26, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=9, adjust=False).mean()
    hist = macd - signal
    return macd.iloc[-1], signal.iloc[-1], hist.iloc[-1]

def get_fundamentals(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "pe_ratio": info.get("trailingPE", "N/A"),
            "pb_ratio": info.get("priceToBook", "N/A"),
            "ps_ratio": info.get("priceToSalesTrailing12Months", "N/A"),
            "peg_ratio": info.get("pegRatio", "N/A"),
            "roa": info.get("returnOnAssets", "N/A"),
            "roe": info.get("returnOnEquity", "N/A")
        }
    except Exception as e:
        print(f"Warning: Could not fetch fundamentals for {ticker}: {str(e)}")
        return {
            "pe_ratio": "N/A",
            "pb_ratio": "N/A",
            "ps_ratio": "N/A",
            "peg_ratio": "N/A",
            "roa": "N/A",
            "roe": "N/A"
        }

def get_stock_data(ticker, window):
    try:
        # Get historical data with retry mechanism
        hist_data = get_stock_data_with_retry(ticker)
        
        price = round(hist_data.iloc[-1].Close, 2)
        sma = round(hist_data.Close.rolling(window=window).mean().iloc[-1], 2)
        ema = round(hist_data.Close.ewm(span=window, adjust=False).mean().iloc[-1], 2)
        
        # Calculate RSI
        delta = hist_data.Close.diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        ema_up = up.ewm(com=14-1, adjust=False).mean()
        ema_down = down.ewm(com=14-1, adjust=False).mean()
        rs = ema_up / ema_down
        rsi = round(100 - (100 / (1 + rs)).iloc[-1], 2)
        
        # Calculate MACD
        short_ema = hist_data.Close.ewm(span=12, adjust=False).mean()
        long_ema = hist_data.Close.ewm(span=26, adjust=False).mean()
        macd = short_ema - long_ema
        signal = macd.ewm(span=9, adjust=False).mean()
        macd_hist = macd - signal
        macd_val, signal_line, macd_hist = [round(v.iloc[-1], 2) for v in (macd, signal, macd_hist)]
        
        fundamentals = get_fundamentals(ticker)
        
        # Generate report with Gemini
        prompt = f"""
You are a helpful financial assistant. Generate a clean Markdown report for a retail investor. Avoid backslashes or code formatting. Use standard bold headers and readable bullet points.

### {ticker} Stock Analysis

**Valuation & Profitability Metrics:**
- P/E Ratio: {fundamentals['pe_ratio']}
- P/B Ratio: {fundamentals['pb_ratio']}
- P/S Ratio: {fundamentals['ps_ratio']}
- PEG Ratio: {fundamentals['peg_ratio']}
- Return on Assets (ROA): {fundamentals['roa']}
- Return on Equity (ROE): {fundamentals['roe']}

**Technical Indicators:**
- Latest Price: ${price}
- {window}-day SMA: {sma}
- {window}-day EMA: {ema}
- RSI: {rsi}
- MACD Line: {macd_val}
- MACD Signal Line: {signal_line}
- MACD Histogram: {macd_hist}
"""

        response = model.generate_content(
            contents=[{"role": "user", "parts": [{"text": prompt}]}],
            generation_config={"temperature": 0}
        )
        
        # Prepare chart data
        chart_data = hist_data.copy()
        chart_data['SMA'] = chart_data['Close'].rolling(window=window).mean()
        chart_data['EMA'] = chart_data['Close'].ewm(span=window, adjust=False).mean()
        chart_data = chart_data.reset_index()
        chart_data['Date'] = chart_data['Date'].dt.strftime('%Y-%m-%d')
        
        return {
            "report": response.text,
            "chart_data": chart_data[['Date', 'Close', 'SMA', 'EMA']].to_dict('records'),
            "ticker": ticker,
            "price": price,
            "success": True
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# If running this file directly as an API (using Flask)
if __name__ == "__main__":
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    
    @app.route('/api/stock_data', methods=['POST'])
    def api_stock_data():
        data = request.json
        company_input = data.get('company_input', '')
        window = data.get('window', 14)
        
        try:
            ticker = get_ticker_from_name(company_input)
            result = get_stock_data(ticker, window)
            return jsonify(result)
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    
    app.run(debug=True, port=5000)
