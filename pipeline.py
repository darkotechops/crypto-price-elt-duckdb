import requests
import json
import os
from transfrom import load_raw_data, transform_data 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
# Note: Since CoinGecko is a public API, no key is needed here.
# For a secured API, you would use: os.getenv("API_KEY")
API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_last_updated_at=true"
RAW_DATA_FILE = 'raw_crypto_data.json' 

def extract_data(api_url):
    """Fetches data from the API and saves the raw JSON to a temporary file."""
    print("1. Extraction Step...")
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        raw_data = response.json()
        
        with open(RAW_DATA_FILE, "w") as f:
            json.dump(raw_data, f, indent=4)
            
        print(f"Extraction successful. Raw data saved to {RAW_DATA_FILE}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error during API extraction: {e}")
        return False

def run_pipeline():
    """Runs the full ELT pipeline sequence: Extract -> Load -> Transform -> Cleanup."""
    print("--- Starting ELT Pipeline ---")
    
    # 1. Extract
    if not extract_data(API_URL):
        print("--- Pipeline FAILED at Extraction ---")
        return
        
    # 2. Load Raw Data
    print("2. Raw Load Step...")
    if not load_raw_data():
        print("--- Pipeline FAILED at Raw Load ---")
        return

    # 3. Transform Data
    print("3. Transformation Step...")
    transform_data()

    # 4. Clean up the temporary raw file
    if os.path.exists(RAW_DATA_FILE):
        os.remove(RAW_DATA_FILE)
    
    print("--- Pipeline Finished Successfully ---")

if __name__ == "__main__":
    run_pipeline()