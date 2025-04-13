# Stock Report

A Streamlit web app that combines real-time stock analysis and report with AI-generated insights from Google Gemini API to provide users with smart, human-like financial recommendations based on ticker input.

## Features

- Real-time stock price data retrieval via Yahoo Finance API
- Technical analysis including SMA, EMA, RSI, and MACD
- Fundamental analysis with key financial metrics
- AI-generated reports using Google's Gemini model
- Interactive charts to visualize stock performance
- Comprehensive company search by name or ticker symbol

## Setup Instructions

### Prerequisites

- Python 3.9+
- pip (Python package installer)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/stock_report.git
   cd stock_report
   ```

2. Create and activate a virtual environment:

   **Windows:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

   **macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install backend dependencies:
   ```bash
   pip install -r requirements-backend.txt
   ```

4. Install frontend dependencies:
   ```bash
   pip install -r requirements-frontend.txt
   ```

### Running the Application

1. Make sure your virtual environment is activated.

2. Start the backend server:
   ```bash
   python backend-code.py
   ```

3. In a new terminal, activate the virtual environment again and start the frontend:
   ```bash
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   
   streamlit run frontend-code.py
   ```

4. Open your browser and navigate to http://localhost:8501

## Troubleshooting

### Yahoo Finance API Issues

If you encounter errors like "No price data found, symbol may be delisted" when querying stock data:

1. **Update yfinance**: The Yahoo Finance API occasionally changes, requiring updates to the yfinance library.
   ```bash
   pip install --upgrade yfinance
   ```

2. **Network Issues**: Ensure you have a stable internet connection and can access finance.yahoo.com in your browser.

3. **Rate Limiting**: Yahoo Finance may rate-limit excessive requests. The application includes a retry mechanism, but you may need to wait between queries if you're making many requests.

4. **Proxy Settings**: If you're behind a corporate firewall, check your proxy settings or try using the application on a different network.

### Virtual Environment Issues

- **Command not found**: If you get "venv not found" errors, ensure Python's venv module is installed:
  ```bash
  # Windows
  python -m pip install --user virtualenv
  
  # macOS/Linux
  python3 -m pip install --user virtualenv
  ```
  
- **Activation issues**: If activation doesn't work, check your system's execution policy (Windows) or file permissions (Unix).

### Other Common Issues

- **Module not found errors**: Ensure you've installed all dependencies from both requirements files.
- **Port already in use**: If port 5000 (backend) or 8501 (frontend) is already in use, you may need to terminate other applications or specify different ports.

## Usage Guide

1. Enter a company name or ticker symbol in the search box
2. Select the time period for technical analysis (default: 14 days)
3. Click "Generate Report" to retrieve data and create analysis
4. View the AI-generated financial insights and technical charts
5. Use the information to make more informed investment decisions

## Dependencies

### Backend
- Flask: Web server framework
- pandas: Data manipulation
- yfinance: Yahoo Finance API client
- google-generativeai: Google Gemini API client

### Frontend
- Streamlit: Interactive web application framework
- plotly: Interactive charts
- requests: HTTP client
- pandas: Data manipulation

## License

[Include your license information here]

## Contributors

[List contributors or add contribution guidelines]
