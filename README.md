# Weather ETL Pipeline with Apache Airflow

## 📌 Project Overview

This project is an ETL (Extract, Transform, Load) pipeline that extracts weather data from [Meteo.it](https://www.meteo.it) using **BeautifulSoup** and **Pandas**, transforms it, and loads it into an **SQLite database**. The entire process is managed using **Apache Airflow** and containerized with **Docker Compose**.

## 🏗️ Tech Stack

- **Python**: Data extraction and transformation
- **BeautifulSoup**: Web scraping from Meteo.it
- **Pandas**: Data cleaning and transformation
- **SQLite**: Storing the transformed data
- **Apache Airflow**: Orchestrating and scheduling the ETL process
- **Docker Compose**: Containerizing and managing services

## 🚀 Project Structure

```
├── dags
│   ├── meteo_etl.py       # Airflow DAG definition
│   │   spider.py          # Web scraping script using BeautifulSoup
│   ├── data               # Directory for storing intermediate CSV files
│   ├── logs               # Airflow logs
│   ├── plugins            # Airflow plugins (if needed)
├── docker-compose.yml     # Docker Compose configuration
└── README.md              # Project documentation
```

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-repo/weather-etl.git
cd weather-etl
```

### 2️⃣ Start the Airflow environment

```bash
docker compose up -d
```

This will start Airflow (webserver, scheduler) and PostgreSQL for metadata storage.

### 3️⃣ Access the Airflow UI

Once the containers are running, open **Airflow UI** at:

```
http://localhost:8080
```

Login with:

- **Username**: `admin`
- **Password**: `admin`

### 4️⃣ Trigger the DAG manually

1. Locate the `` DAG.
2. Click on **Trigger DAG** to start the ETL process.

## 🛠 How the ETL Pipeline Works

### 📥 **Extract**

- `MeteoSpider` (in `spider.py`) scrapes weather data from **Meteo.it**.
- Extracted data is saved as CSV files in the `/opt/airflow/data` directory.

### 🔄 **Transform**

- Data is cleaned using **Pandas**.
- Missing values are removed, and columns are standardized.

### 📤 **Load**

- The cleaned data is loaded into an **SQLite database** (`meteo.db`).
- The database file is stored inside the Airflow container (`/opt/airflow/data/meteo.db`).

## 🗂 Environment Variables

The **Airflow environment** is configured using `docker-compose.yml`. If needed, modify these settings:

```yaml
  environment:
    - AIRFLOW__CORE__EXECUTOR=LocalExecutor
    - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
    - AIRFLOW__WEBSERVER__DEFAULT_UI_TIMEZONE=Europe/Rome
```

## 🔍 Checking the Database

To inspect the stored data inside the **SQLite database**, enter the Airflow container:

```bash
docker exec -it <container_id> /bin/bash
```

Then, open SQLite and query the database:

```bash
sqlite3 /opt/airflow/data/meteo.db
SELECT * FROM meteo_data LIMIT 5;
```

## 🛑 Stopping the Containers

To stop the Airflow environment, run:

```bash
docker compose down
```

## 📌 Future Improvements

- Store data in **PostgreSQL** instead of SQLite.
- Improve error handling and logging.
- Automate daily historical weather data collection.

---

💡 **Contributions & Issues** If you encounter any issues or have suggestions, feel free to open an issue or contribute! 🚀

