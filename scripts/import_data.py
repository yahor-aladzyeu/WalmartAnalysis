import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import logging
import json

# Logging configuration
logging.basicConfig(filename='import_data.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def load_config(config_path='config.json'):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

def import_data(cleaned_data_path, config):
    username = config['username']
    password = config['password']
    host = config['host']
    database = config['database']
    table_name = config['table_name']
    DATABASE_URI = f'mysql+pymysql://{username}:{password}@{host}/{database}'

    try:
        # Load the "Walmart_cleaned.csv"
        df = pd.read_csv(cleaned_data_path)
        logging.info("Cleaned CSV file loaded")

        # Create the database engine
        engine = create_engine(DATABASE_URI)
        logging.info("Database engine created")

        # Import data into MySQL
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
        logging.info("Data imported into table %s in database %s", table_name, database)

        # Display success message
        print(f"Success: Data has been imported into the table {table_name} in the database {database}.")
        logging.info("Success: Data has been imported into the table %s in the database %s", table_name, database)

    except FileNotFoundError as e:
        logging.error("Error: File not found - %s", e)
        print(f"Error: File not found - {e}")

    except pd.errors.EmptyDataError as e:
        logging.error("Error: CSV file is empty - %s", e)
        print(f"Error: CSV file is empty - {e}")

    except SQLAlchemyError as e:
        logging.error("Error connecting to the database or importing data - %s", e)
        print(f"Error connecting to the database or importing data - {e}")

    except Exception as e:
        logging.error("An unexpected error occurred - %s", e)
        print(f"An unexpected error occurred - {e}")

if __name__ == "__main__":
    config = load_config()
    import_data('Walmart_cleaned.csv', config)
