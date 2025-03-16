import sqlite3
import pandas as pd
from logger import logger

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("meteo.db")
        self.cursor = self.conn.cursor()

    def create_table_from_csv(self, csv_file_path):
        df = pd.read_csv(csv_file_path)
        table_name = csv_file_path.split("/")[-1].split(".")[0]

        df.to_sql(table_name, self.conn, if_exists="replace", index=False)

        # Leggi i dati dalla tabella
        df_check = pd.read_sql(f"SELECT * FROM {table_name}", self.conn)
        logger.info(f"Table {table_name} created with {len(df_check)} records")

        return df_check


    def query(self, query):
        return pd.read_sql_query(query, self.conn)

    def close(self):
        self.conn.close()
