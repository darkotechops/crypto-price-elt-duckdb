import duckdb
import os

DATABASE_FILE = 'crypto_data.db'
RAW_DATA_FILE = 'raw_crypto_data.json' 

def load_raw_data():
    """Connects to DuckDB and loads the raw JSON file into a staging table."""
    
    if not os.path.exists(RAW_DATA_FILE):
        print(f"Error: Raw data file '{RAW_DATA_FILE}' not found.")
        return False
        
    con = duckdb.connect(DATABASE_FILE) 
    
    load_query = f"""
    CREATE OR REPLACE TABLE raw_staging AS
    SELECT 
        *, 
        now() AS load_timestamp 
    FROM read_json_auto('{RAW_DATA_FILE}', records=True); 
    """
    
    try:
        con.sql(load_query)
        con.close()
        print("Raw data loaded to 'raw_staging' table.")
        return True
    except Exception as e:
        print(f"Error loading to DuckDB: {e}")
        con.close()
        return False

def transform_data():
    """Transforms raw data into a clean, analytical Fact table."""
    con = duckdb.connect(DATABASE_FILE)
    
    # SQL Transformation: Un-nest JSON and structure the data
    transform_query = """
    CREATE OR REPLACE TABLE fact_crypto_prices AS
    SELECT
        CAST(load_timestamp AS TIMESTAMP) AS pipeline_load_ts,
        'bitcoin' AS currency,
        raw_staging.bitcoin.usd AS price_usd, -- Un-nesting the USD price
        to_timestamp(raw_staging.bitcoin.last_updated_at) AS last_updated_ts 
    FROM raw_staging;
    """
    
    try:
        con.sql(transform_query) 
        
        # Simple Data Quality Check
        negative_check = con.sql("SELECT COUNT(*) FROM fact_crypto_prices WHERE price_usd <= 0").fetchone()[0]
        if negative_check > 0:
            print(f"DQ ALERT: Found {negative_check} price records that are zero or negative.")
            
        con.close()
        print("!! Data transformed and loaded into 'fact_crypto_prices'.")
    except Exception as e:
        print(f"Error during transformation: {e}")
        con.close()