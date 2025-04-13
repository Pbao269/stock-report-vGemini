import streamlit as st
import requests
import json

# API endpoint
BACKEND_URL = "http://localhost:5000/api/stock_data"

# Minimal inputs without titles or labels
company_input = st.text_input("", placeholder="Enter company name or ticker").upper()
window = st.slider("", 5, 50, 14, label_visibility="collapsed")

if company_input:
    try:
        # Send request to backend
        response = requests.post(
            BACKEND_URL,
            json={"company_input": company_input, "window": window},
            headers={"Content-Type": "application/json"}
        )
        
        # Display raw JSON data without any formatting
        st.json(response.json())
            
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")
