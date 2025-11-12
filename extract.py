import requests
import json

def extract_data(api_url):
    """Fetches data from the API and returns the raw JSON."""
    try:
        response = requests.get(api_url)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status() 
        print("Extraction successful.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during API extraction: {e}")
        return None

# CoinGecko API for Bitcoin price
if __name__ == "__main__":
    COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_last_updated_at=true"
    raw_data = extract_data(COINGECKO_URL)

    # Save raw data to a JSON file 
    if raw_data:
        with open("raw_crypto_data.json", "w") as f:
            json.dump(raw_data, f, indent=4)
        print("Raw data saved to raw_crypto_data.json")