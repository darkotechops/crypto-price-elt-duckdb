<!--
  Polished README for the Crypto Price ELT Pipeline
  Rewritten to be clearer, actionable, and Windows-friendly.
-->

# 🚀 Crypto Price ELT Pipeline (Python & DuckDB)

![Python](https://img.shields.io/badge/python-3.8%2B-blue) ![DuckDB](https://img.shields.io/badge/duckdb-0.8.0-lightgrey) ![License: MIT](https://img.shields.io/badge/license-MIT-green)

A compact, local ELT pipeline that fetches live cryptocurrency prices from the CoinGecko API, stores raw JSON in DuckDB, and produces a small analytical fact table. Built as a portfolio project to demonstrate data-engineer skills.

Summary
- Extract: fetches live price data (CoinGecko REST API)
- Load: saves raw JSON and ingests into a DuckDB staging table
- Transform: SQL-based unnesting and cleaning into `fact_crypto_prices`

---

## 🌟 Highlights

| Feature | Skill Demonstrated |
|---|---|
| Modular pipeline | Separation of orchestration (`pipeline.py`) and transformation (`transform.py`) |
| Live data ingestion | HTTP API integration with `requests` |
| SQL transforms | DuckDB SQL for JSON unnesting and timestamp conversions |
| Reproducible env | `venv` + `requirements.txt` and `.env` handling |
| Basic DQ | Simple validation checks in transform step |

---

## 🏗 Architecture & Data Flow

Flow: CoinGecko API → `pipeline.py` (extract) → DuckDB raw staging → DuckDB transform → `fact_crypto_prices`

### Data model (fact_crypto_prices)

| Column | Type | Description |
|---|---:|---|
| pipeline_load_ts | TIMESTAMP | When the pipeline executed (metadata) |
| currency | VARCHAR | Crypto asset (e.g., `bitcoin`) |
| price_usd | REAL | Cleaned price in USD |
| last_updated_ts | TIMESTAMP | API timestamp converted from epoch |

---

## 💻 Tech stack

- Python 3.8+
- DuckDB (local analytical DB)
- Libraries: `requests`, `pandas`, `duckdb`, `python-dotenv`

---

## ▶️ Quickstart

Clone the repo and create a virtual environment, then install dependencies.

On Windows PowerShell:

```powershell
git clone [YOUR_REPOSITORY_URL]
cd de_api_project
python -m venv venv
.\venv\Scripts\Activate.ps1    # PowerShell
pip install -r requirements.txt
type nul > .env                   # create empty .env (optional)
python pipeline.py
```

macOS / Linux (bash):

```bash
git clone [YOUR_REPOSITORY_URL]
cd de_api_project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
touch .env
python pipeline.py
```

If the pipeline completes successfully you should see messages like:

- Extraction: raw JSON saved to `raw_crypto_data.json`
- Raw load: data inserted into `raw_staging` table
- Transform: data written to `fact_crypto_prices` in `crypto_data.db`

You can inspect results quickly with:

```powershell
python analytics.py
```

---

## Example output (abbreviated)

```
--- Starting ELT Pipeline ---
1. Extraction Step...
Extraction successful. Raw data saved to raw_crypto_data.json
2. Raw Load Step...
Raw data loaded to 'raw_staging' table.
3. Transformation Step...
!! Data transformed and loaded into 'fact_crypto_prices'.
--- Pipeline Finished Successfully ---
```

---

## 🔧 Implementation notes & tips

- Timestamps: DuckDB's `to_timestamp()` is used to convert epoch values to TIMESTAMP.
- JSON fields: DuckDB SQL can directly access nested JSON from the raw staging table.
- Idempotency: Current demo appends rows. For production, consider upsert logic or dedup keys.
- Logging & errors: The pipeline logs progress and exits on fatal errors—extend logging as needed.

---

## ✅ Future improvements

- Add orchestration (Airflow) for scheduling and retries.
- Add automated data validation (Great Expectations or custom checks).
- Containerize the pipeline and add CI/CD (GitHub Actions).
- Support multi-asset ingestion and incremental loading.

---

## 🗂 Project structure

Files you’ll find:

```
pipeline.py        # Orchestrates the ELT steps
transform.py       # DuckDB SQL transforms & validations
analytics.py       # Quick inspection / demo queries
requirements.txt   # Python dependencies
.env               # Environment variables (not checked-in)
.gitignore         # Excludes crypto_data.db, raw JSON, .env, venv
raw_crypto_data.json  # Raw API dump (temporary)
crypto_data.db        # DuckDB file (output)
```

---

## Author

Darko Kostovski

---
