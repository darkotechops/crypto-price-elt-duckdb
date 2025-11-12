import duckdb
import pandas as pd
import matplotlib.pyplot as plt

DATABASE_FILE = 'crypto_data.db'

def visualize_data():
    # ... (connection and query code remains the same as view_data) ...
    con = duckdb.connect(DATABASE_FILE)
    df = con.sql("SELECT * FROM fact_crypto_prices ORDER BY pipeline_load_ts ASC").df()
    con.close()

    # --- Plotting ---
    plt.figure(figsize=(10, 6))
    plt.plot(df['last_updated_ts'], df['price_usd'], marker='o')
    plt.title('Bitcoin Price Trend from ELT Pipeline')
    plt.xlabel('Timestamp')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    visualize_data()