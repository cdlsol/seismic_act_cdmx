import pandas as pd
from time import time
from sqlalchemy import create_engine
import argparse

def main(params):

    #Connect to DB
    pg_user = params.user
    pg_password  = params.password
    pg_host = params.host
    pg_port = params.port
    pg_db = params.db
    pg_table = params.table
    csv_path = params.csv_path

    #Connection
    engine = create_engine(f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}")
    con = engine.connect()

    #Iterator
    df_iter = pd.read_csv(csv_path, iterator=True, chunksize=100)
    df = next(df_iter)

    # Transform Data
    df.Fecha = pd.to_datetime(df.Fecha, dayfirst=True).dt.date
    df["Fecha UTC"] = pd.to_datetime(df["Fecha UTC"], dayfirst=True).dt.date
    df.Hora = pd.to_datetime(df.Hora, format="%H:%M:%S").dt.time
    df["Hora UTC"] = pd.to_datetime(df["Hora UTC"], format="%H:%M:%S").dt.time
    df.info()

    #Data to DB
    df.head(0).to_sql(con = con, name = pg_table, if_exists = "replace")
    df.to_sql(con = con, name = pg_table, if_exists = "append")

    #Iterate through each chunk, transform and add to table
    try:
        while True:
            t_start = time()
            df = next(df_iter)
        
            df.Fecha = pd.to_datetime(df.Fecha, dayfirst=True).dt.date
            df["Fecha UTC"] = pd.to_datetime(df["Fecha UTC"], dayfirst=True).dt.date
            df.Hora = pd.to_datetime(df.Hora, format="%H:%M:%S").dt.time
            df["Hora UTC"] = pd.to_datetime(df["Hora UTC"], format="%H:%M:%S").dt.time
            
            df.to_sql(con = con, name = pg_table, if_exists = "append")
        
            end_time = time()
            print("New Records Added! {}".format(end_time - t_start))
    except StopIteration:
        print("All chunks have been processed successfully.")

if __name__ == "__main__":

    parser = argparse.ArgumentParser( description='Data ingest to Seismic Table',)
    parser.add_argument('--user', help="Database User")      # option that takes a value
    parser.add_argument('--password', help="Database Password")      # option that takes a value
    parser.add_argument('--host', help="Database Host")      # option that takes a value
    parser.add_argument('--port', help="Database Port")      # option that takes a value
    parser.add_argument('--db', help="Database Name")      # option that takes a value
    parser.add_argument('--table', help="Database Table")      # option that takes a value
    parser.add_argument('--csv_path', help="CSV Path")      # option that takes a value

    params = parser.parse_args()

    main(params)