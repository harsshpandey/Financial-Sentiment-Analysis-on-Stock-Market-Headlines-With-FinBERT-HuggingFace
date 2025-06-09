import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check Response:", response.json())

def test_single_analysis():
    """Test single headline analysis"""
    headline = "Apple stock rises after strong quarterly earnings"
    response = requests.post(
        f"{BASE_URL}/analyze",
        json={"headline": headline}
    )
    print("\nSingle Analysis Response:", response.json())

def test_batch_analysis():
    """Test batch headline analysis"""
    headlines = [
        "Tesla announces new factory in Asia",
        "Microsoft beats revenue expectations",
        "Oil prices drop amid supply concerns"
    ]
    response = requests.post(
        f"{BASE_URL}/analyze-batch",
        json={"headlines": headlines}
    )
    print("\nBatch Analysis Response:", response.json())

if __name__ == "__main__":
    print("Testing Financial Sentiment Analysis API...")
    test_health()
    test_single_analysis()
    test_batch_analysis() 