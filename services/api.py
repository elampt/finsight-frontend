import requests
import os
import streamlit as st
from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

# Load the API base URL from Streamlit secrets
# This is typically set in the Streamlit Cloud or local secrets.toml file
# API_BASE_URL = st.secrets["API_BASE_URL"]

# Uncomment the line below to use a local API for testing
# API_BASE_URL = "http://localhost:8000"

# Try Streamlit secrets first (for deployed environment), fall back to .env
try:
    API_BASE_URL = st.secrets["API_BASE_URL"]
except (KeyError, FileNotFoundError):
    API_BASE_URL = os.getenv("API_BASE_URL")
    if not API_BASE_URL:
        st.error("API_BASE_URL not found in st.secrets or .env file")
        st.stop()


def signup_user(name, email, password):
    try:
        response = requests.post(f"{API_BASE_URL}/user/signup", json={
            "name": name,
            "email": email,
            "password": password
        })
        return response.status_code == 201
    except Exception as e:
        print(f"Error during signup: {e}")
        return False

def login_user(email, password):
    try:
        response = requests.post(f"{API_BASE_URL}/user/login", data={
            "username": email,
            "password": password
            })
        if response.status_code == 200:
            return response.json().get("access_token")
        return None
    except Exception as e:
        print(f"Error during login: {e}")
        return None
    
def get_holdings(token):
    try:
        response = requests.get(f"{API_BASE_URL}/holdings/profit-loss", headers={
            "Authorization": f"Bearer {token}"
        })
        return response.json() if response.status_code == 200 else []
    except Exception as e:
        print(f"Error fetching holdings: {e}")
        return []
    
def add_holding(token, stock_symbol, shares, purchase_cost, purchase_date):
    try:
        response = requests.post(f"{API_BASE_URL}/holdings/add", headers={
            "Authorization": f"Bearer {token}"}, json={
            "stock_symbol": stock_symbol,
            "shares": shares,
            "purchase_cost": purchase_cost,
            "purchase_date": purchase_date
        })
        return response.status_code == 201
    except Exception as e:
        print(f"Error adding holding: {e}")
        return False
    
def delete_holding(token, holding_id):
    try:
        response = requests.delete(f"{API_BASE_URL}/holdings/delete/{holding_id}", headers={
            "Authorization": f"Bearer {token}"
        })
        return response.status_code == 204
    except Exception as e:
        print(f"Error deleting holding: {e}")
        return False

def update_holding(token, holding_id, shares, purchase_cost, purchase_date):
    try:
        response = requests.put(f"{API_BASE_URL}/holdings/update/{holding_id}", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "shares": shares,
            "purchase_cost": purchase_cost,
            "purchase_date": purchase_date
        })
        return response.status_code == 200
    except Exception as e:
        print(f"Error updating holding: {e}")
        return False

def get_stock_symbols():
    """
    Fetch all stock symbols from the API.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/holdings/stocks/symbols")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching stock symbols: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching stock symbols: {e}")
        return []

    
def get_news_sentiment(token):
    try:
        response = requests.get(f"{API_BASE_URL}/holdings/news-sentiment", headers={
            "Authorization": f"Bearer {token}"
        })
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"Error fetching news sentiment: {e}")
        return None