# 🚕 NYC Yellow Taxi Data Ingestion Project

A fully containerized ETL pipeline for ingesting, storing, and analyzing NYC Yellow Taxi trip data using:

- 🐘 PostgreSQL (for structured data storage)
- 📊 pgAdmin (for managing the database)
- 📓 Jupyter Notebook (for data exploration and Python-based ETL)
- 🐳 Docker Compose (for service orchestration)

---

## 📦 Project Overview

This project demonstrates how to build a complete local data pipeline from scratch:

1. Download NYC Taxi data (Parquet format)
2. Convert and ingest data into PostgreSQL using Python and Pandas
3. Use SQL and Jupyter to explore and analyze the data
4. Access Postgres via a clean GUI with pgAdmin

Ideal for data engineers or data science learners looking to combine **Docker, SQL, and Python** in a real-world context.

---

## 🧱 Tech Stack

| Tool          | Purpose                          |
|---------------|----------------------------------|
| Docker        | Container orchestration          |
| PostgreSQL    | Data warehouse / structured DB   |
| pgAdmin       | GUI for managing PostgreSQL      |
| Jupyter       | Notebook-based data processing   |
| Pandas        | CSV/Parquet handling and ETL     |
| SQLAlchemy    | Python–Postgres bridge           |
| psycopg2      | PostgreSQL DB adapter for Python |

---

## 📁 Project Structure

nyc_taxi_ingestion/
├── docker-compose.yml # Dockerized services
├── notebooks/ # Jupyter notebooks (ETL, EDA)
├── data/ # Raw data files (excluded from Git)
├── requirements.txt # Python dependencies
├── pendo_tracking.py # Pendo Track Events sent by the ingestion steps
├── .gitignore # Excludes data/.env/state
└── README.md # Project documentation

yaml
Copy
Edit

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/nyc-taxi-ingestion.git
cd nyc-taxi-ingestion
2. Start Docker Containers
bash
Copy
Edit
docker compose up -d
This will start:

PostgreSQL (on port 5432)

Jupyter Notebook (on port 8888)

pgAdmin (on port 5050)

3. Access Services
Tool	URL
Jupyter	http://localhost:8888
pgAdmin	http://localhost:5050

📌 Default pgAdmin login (from docker-compose.yml):

makefile
Copy
Edit
Email: admin@example.com
Password: admin123
📌 Postgres credentials:

makefile
Copy
Edit
Username: taxi
Password: taxi
Database: nyc_taxi
📥 Data Ingestion Steps
Each step reports a Pendo Track Event with track_event() from pendo_tracking.py, so run the snippets from a notebook in the repo root (/home/jovyan/work in Jupyter).

To send the events, set PENDO_TRACK_EVENT_SECRET (plus PENDO_DATA_HOST if your Pendo subscription is not on https://data.pendo.io) in your shell before docker compose up: export PENDO_TRACK_EVENT_SECRET=<secret> in bash, or $env:PENDO_TRACK_EVENT_SECRET = "<secret>" in PowerShell. Keep the secret out of notebooks and committed files. Without it the events are skipped and the steps run as before.

Load Parquet → CSV (first 100K rows for testing):

python
Copy
Edit
import os
import pandas as pd
from pendo_tracking import track_event

# Settings for this run, shared by the steps below
data_month = "2023-01"
parquet_file = f"yellow_tripdata_{data_month}.parquet"
csv_file = f"yellow_tripdata_{data_month}.csv"
table_name = "yellow_taxi_data"

df = pd.read_parquet(parquet_file)
df_sample = df.head(100_000)
df_sample.to_csv(csv_file, index=False)
# Pendo: how much of the source month is kept in the CSV that gets loaded
track_event("trip_parquet_converted_to_csv", {
    "source_file": parquet_file,
    "output_file": csv_file,
    "source_row_count": len(df),
    "rows_exported": len(df_sample),
    "column_count": len(df.columns),
    "data_month": data_month,
    "output_file_size_bytes": os.path.getsize(csv_file),
})
Create Postgres schema:

python
Copy
Edit
from sqlalchemy import inspect

df = pd.read_csv(csv_file)
# if_exists="replace" drops the table and every row loaded so far, so check first
replaced_existing_table = inspect(engine).has_table(table_name)
df.head(0).to_sql(name=table_name, con=engine, if_exists="replace", index=False)
# Pendo: the only record of when the table was (re)created and whether data was wiped
track_event("trip_table_schema_created", {
    "table_name": table_name,
    "if_exists": "replace",
    "replaced_existing_table": replaced_existing_table,
    "column_count": len(df.columns),
    "column_names": ",".join(df.columns),
    "source_file": csv_file,
})
Chunk and ingest data:

python
Copy
Edit
import time

chunksize = 20000
chunks_inserted = 0
rows_ingested = 0
start_time = time.perf_counter()
try:
    for chunk in pd.read_csv(csv_file, chunksize=chunksize):
        chunk.to_sql(name=table_name, con=engine, if_exists="append", index=False)
        chunks_inserted += 1
        rows_ingested += len(chunk)
except Exception as exc:
    # Pendo: each chunk commits on its own, so record where the load stopped, then re-raise
    track_event("trip_data_ingestion_failed", {
        "source_file": csv_file,
        "table_name": table_name,
        "chunksize": chunksize,
        "failed_chunk_number": chunks_inserted + 1,
        "chunks_inserted_before_failure": chunks_inserted,
        "rows_ingested_before_failure": rows_ingested,
        "error_type": type(exc).__name__,
        # pandas 3 wraps database errors and puts the SQL first, so report the cause
        "error_message": str(exc.__cause__ or exc).split("\n", 1)[0][:150],
    })
    raise
# Pendo: once per file, not per chunk
track_event("trip_data_ingestion_completed", {
    "source_file": csv_file,
    "table_name": table_name,
    "if_exists": "append",
    "chunksize": chunksize,
    "chunks_inserted": chunks_inserted,
    "rows_ingested": rows_ingested,
    "duration_seconds": round(time.perf_counter() - start_time, 2),
    "data_month": data_month,
})
📊 Sample Questions to Explore
What’s the average trip duration per hour?

Which pickup locations are busiest?

What’s the distribution of trip distances?

Are there seasonal or hourly trends in ride volume?

📈 Future Enhancements
 Add data visualization (matplotlib, seaborn)

 Automate ingestion of multiple months

 Add indexes or partitioning to improve query performance

 Integrate with Airflow for scheduled ingestion

 Add dashboards using Plotly, Dash, or Metabase

🧠 Learning Goals
This project is a hands-on demonstration of:

Infrastructure-as-code with Docker

Real-world ETL with Python + SQL

Multi-service orchestration and networking

Chunked data ingestion for large datasets

Portfolio-ready data engineering workflows

📎 License
This project is MIT licensed and built for educational purposes.

yaml
Copy
Edit

---

## 🪄 What to Do Now

1. Save this as `README.md` in your project folder.
2. Commit and push:

```bash
git add README.md
git commit -m "Add professional project README"
git push
