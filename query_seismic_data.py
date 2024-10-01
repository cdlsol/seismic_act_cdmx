import pandas as pd
from sqlalchemy import create_engine
import argparse

def query_db(user, password, host, port, db_name, query):
    # Create a SQLAlchemy engine for PostgreSQL
    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}')
    
    # Use pandas to read SQL query into a DataFrame
    try:
        df = pd.read_sql_query(query, engine)
        return df  # Return the DataFrame
    except Exception as e:
        print(f"Error while querying the database: {e}")
    finally:
        engine.dispose()  # Dispose the engine

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Query the PostgreSQL database and load results into a DataFrame')
    parser.add_argument('--user', required=True, help='Database username')
    parser.add_argument('--password', required=True, help='Database password')
    parser.add_argument('--host', required=True, help='Database host')
    parser.add_argument('--port', required=True, help='Database port')
    parser.add_argument('--db', required=True, help='Database name')
    parser.add_argument('--query', required=True, help='SQL query to execute')

    args = parser.parse_args()

    # Call the query function and store results in a DataFrame
    df = query_db(args.user, args.password, args.host, args.port, args.db, args.query)

    # Print the DataFrame
    if df is not None:
        print(df)
