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
Load Parquet → CSV (first 100K rows for testing):

python
Copy
Edit
import pandas as pd
df = pd.read_parquet("yellow_tripdata_2023-01.parquet")
df.head(100_000).to_csv("yellow_tripdata_2023-01.csv", index=False)
Create Postgres schema:

python
Copy
Edit
df = pd.read_csv("yellow_tripdata_2023-01.csv")
df.head(0).to_sql(name="yellow_taxi_data", con=engine, if_exists="replace", index=False)
Chunk and ingest data:

python
Copy
Edit
chunksize = 20000
for chunk in pd.read_csv("yellow_tripdata_2023-01.csv", chunksize=chunksize):
    chunk.to_sql(name="yellow_taxi_data", con=engine, if_exists="append", index=False)
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
