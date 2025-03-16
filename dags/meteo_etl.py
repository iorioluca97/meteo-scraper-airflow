from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import sqlite3
import sys

sys.path.append('/opt/airflow/dags')
from spider import MeteoSpider


# Definizione del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 15),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'meteo_etl',
    default_args=default_args,
    description='ETL per dati meteo in SQLite',
    schedule_interval=timedelta(hours=1),  # Esegue ogni ora
)

# Funzione per estrarre i dati
def extract_data():
    spidy = MeteoSpider()
    df_regions, df_news = spidy.run()
    
    # Salviamo i dati come CSV temporanei
    df_regions.to_csv('/tmp/regions.csv', index=False)
    df_news.to_csv('/tmp/news.csv', index=False)

# Funzione per trasformare i dati
def transform_data():
    df = pd.read_csv('/tmp/regions.csv')
    
    # Esempio di trasformazione: rimuovere valori nulli
    df.dropna(inplace=True)
    
    # Salviamo il dataset pulito
    df.to_csv('/tmp/regions_cleaned.csv', index=False)

# Funzione per caricare i dati in SQLite
def load_data():
    conn = sqlite3.connect('/tmp/meteo.db')
    df = pd.read_csv('/tmp/regions_cleaned.csv')
    
    # Carichiamo i dati in una tabella SQLite
    df.to_sql('meteo_data', conn, if_exists='replace', index=False)
    
    conn.close()

# Definizione delle task di Airflow
task_extract = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

task_transform = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

task_load = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

# Definizione della sequenza delle task
task_extract >> task_transform >> task_load
