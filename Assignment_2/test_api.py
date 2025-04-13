# test_api.py
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

def test_create_item():
    """Test creating a new item"""
    url = f"{BASE_URL}/items/"
    data = {
        "code": "I-001",
        "name": "History Book",
        "unit": "Pcs",
        "description": "Books that tell the history of the ancient"
    }
    response = requests.post(url, json=data)
    print(f"Create Item Response: {response.status_code}")
    print(response.json())
    return response.json()

def test_create_purchase():
    """Test creating a purchase with details"""
    url = f"{BASE_URL}/purchase/"
    data = {
        "code": "P-001",
        "date": "2025-01-01",
        "description": "Initial purchase",
        "details": [
            {
                "item_code": "I-001",
                "quantity": 10,
                "unit_price": 60000
            }
        ]
    }
    response = requests.post(url, json=data)
    print(f"Create Purchase Response: {response.status_code}")
    print(response.json())
    return response.json()

def test_create_second_purchase():
    """Test creating a second purchase"""
    url = f"{BASE_URL}/purchase/"
    data = {
        "code": "P-002",
        "date": "2025-02-01",
        "description": "Restock",
        "details": [
            {
                "item_code": "I-001",
                "quantity": 10,
                "unit_price": 50000
            }
        ]
    }
    response = requests.post(url, json=data)
    print(f"Create Second Purchase Response: {response.status_code}")
    print(response.json())
    return response.json()

def test_create_sell():
    """Test creating a sell with details"""
    url = f"{BASE_URL}/sell/"
    data = {
        "code": "S-001",
        "date": "2025-03-01",
        "description": "Sell history books to library",
        "details": [
            {
                "item_code": "I-001",
                "quantity": 15
            }
        ]
    }
    response = requests.post(url, json=data)
    print(f"Create Sell Response: {response.status_code}")
    print(response.json())
    return response.json()

def test_get_item():
    """Test getting an item to check updated stock"""
    url = f"{BASE_URL}/items/I-001/"
    response = requests.get(url)
    print(f"Get Item Response: {response.status_code}")
    print(response.json())
    return response.json()

def test_get_report():
    """Test getting a report for an item"""
    url = f"{BASE_URL}/report/I-001/?start_date=2025-01-01&end_date=2025-03-31"
    response = requests.get(url)
    print(f"Get Report Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

if __name__ == "__main__":
    # Run the tests in sequence
    test_create_item()
    test_create_purchase()
    test_create_second_purchase()
    test_create_sell()
    test_get_item()
    test_get_report()