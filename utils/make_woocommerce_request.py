# utils/make_woocommerce_request.py
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("WOOCOMMERCE_API_ROUTE")
CLIENT_KEY = os.getenv("WOOCOMMERCE_CLIENT_KEY")
CLIENT_SECRET = os.getenv("WOCOMMERCE_SECRET_KEY")

def make_woocommerce_request(endpoint, method="GET", data=None):
    """
    Makes a request to the WooCommerce API.
    
    Args:
        endpoint (str): The endpoint to make the request to.
        method (str): The HTTP method to use (defaults to "GET").
        data (dict, optional): The data to send with the request.
    
    Returns:
        requests.Response: The raw response from the API.
    
    Raises:
        ValueError: If invalid method provided.
        requests.RequestException: If the request fails.
    """
    if not all([API_URL, CLIENT_KEY, CLIENT_SECRET]):
        raise ValueError("WooCommerce API credentials not properly configured")

    url = f"{API_URL.rstrip('/')}/{endpoint.lstrip('/')}"
    headers = {'Content-Type': 'application/json'}
    
    try:
        if method == "GET":
            response = requests.get(
                url,
                auth=(CLIENT_KEY, CLIENT_SECRET),
                params=data,
                headers=headers
            )
        elif method in ["POST", "PUT", "DELETE"]:
            response = requests.request(
                method,
                url,
                auth=(CLIENT_KEY, CLIENT_SECRET),
                data=json.dumps(data) if data else None,
                headers=headers
            )
        else:
            raise ValueError(f"Invalid method provided: {method}")
        
        response.raise_for_status()
        return response
        
    except requests.RequestException as e:
        print(f"WooCommerce API request failed: {str(e)}")
        raise