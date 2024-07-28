import os
import logging
from sqlalchemy import create_engine, text
import pandas as pd
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_file='config.json'):
    """Loads the JSON configuration file."""
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
        logging.info("Configuration loaded successfully.")
        print("Configuration loaded successfully.")
        return config
    except Exception as e:
        logging.error(f"Failed to load configuration: {e}")
        print(f"Failed to load configuration: {e}")
        raise

def create_db_engine(config):
    """Creates a database engine based on the provided configuration."""
    try:
        db_url = f"mysql+mysqlconnector://{config['username']}:{config['password']}@{config['host']}/{config['database']}"
        engine = create_engine(db_url)
        logging.info("Database engine created successfully.")
        print("Database engine created successfully.")
        return engine
    except Exception as e:
        logging.error(f"Failed to create database engine: {e}")
        print(f"Failed to create database engine: {e}")
        raise

def read_queries(file_path):
    """Reads SQL queries from the specified file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            queries = file.read().split(';')
        # Remove empty queries
        queries = [query.strip() for query in queries if query.strip()]
        logging.info(f"{len(queries)} queries read from {file_path}.")
        print(f"{len(queries)} queries read from {file_path}.")
        return queries
    except Exception as e:
        logging.error(f"Failed to read queries from {file_path}: {e}")
        print(f"Failed to read queries from {file_path}: {e}")
        raise

def execute_queries_and_save_to_csv(queries, engine):
    """Executes SQL queries and saves the results to CSV files."""
    try:
        with engine.connect() as connection:
            for i, query in enumerate(queries):
                result = connection.execute(text(query))
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
                csv_file = f'query_result_{i + 1}.csv'
                df.to_csv(csv_file, index=False)
                logging.info(f"Query {i + 1} executed and results saved to {csv_file}.")
                print(f"Query {i + 1} executed and results saved to {csv_file}.")
    except Exception as e:
        logging.error(f"Failed to execute queries and save results: {e}")
        print(f"Failed to execute queries and save results: {e}")
        raise

if __name__ == '__main__':
    try:
        # Load configuration
        config = load_config()
        # Create database engine
        engine = create_db_engine(config)
        # Read queries from file
        queries = read_queries('queries.sql')
        # Execute queries and save results to CSV
        execute_queries_and_save_to_csv(queries, engine)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
