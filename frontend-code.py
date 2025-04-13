import streamlit as st
import requests
import json
import plotly.graph_objs as go
import pandas as pd

# API endpoint
BACKEND_URL = "http://localhost:5000/api/stock_data"

st.title('📈 Gemini Stock Report Generator')
company_input = st.text_input("Enter company name or ticker (e.g., Apple or AAPL):").upper()
window = st.slider("Select window size for SMA/EMA:", 5, 50, 14)

def plot_interactive_chart(chart_data, ticker, window):
    df = pd.DataFrame(chart_data)
    df['Date'] = pd.to_datetime(df['Date'])
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA'], mode='lines', name=f'{window}-day SMA'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['EMA'], mode='lines', name=f'{window}-day EMA'))

    fig.update_layout(
        title=f'{ticker} Interactive Stock Price Chart',
        xaxis_title='Date',
        yaxis_title='Price ($)',
        hovermode='x unified',
        template='plotly_white'
    )
    return fig

if company_input:
    try:
        # Send request to backend
        response = requests.post(
            BACKEND_URL,
            json={"company_input": company_input, "window": window},
            headers={"Content-Type": "application/json"}
        )
        
        data = response.json()
        
        if data["success"]:
            st.subheader("📊 Gemini Report")
            st.markdown(data["report"], unsafe_allow_html=True)
            
            # Plot chart
            fig = plot_interactive_chart(data["chart_data"], data["ticker"], window)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(f"❌ Error: {data['error']}")
            
    except Exception as e:
        st.error(f"❌ Error connecting to backend service: {str(e)}")
        st.info("Make sure the backend service is running on http://localhost:5000")
