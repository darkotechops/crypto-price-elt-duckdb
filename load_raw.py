# Updated load_raw.py
import duckdb
    
def load_raw_data():
    """Connects to DuckDB and loads raw JSON into a staging table."""
    con = duckdb.connect('crypto_data.db') 
        
    load_query = """
    CREATE OR REPLACE TABLE raw_staging AS
    SELECT 
        *, 
        -- FIX: Use the 'now()' function for the current timestamp/time
        now() AS load_timestamp 
    FROM read_json_auto('raw_crypto_data.json', records=True); 
    """
    
    try:
        con.sql(load_query)
        con.close()
        print("Raw data successfully loaded to 'raw_staging' table in crypto_data.db.")
        return True
    except Exception as e:
        print(f"Error loading to DuckDB: {e}")
        con.close()
        return False