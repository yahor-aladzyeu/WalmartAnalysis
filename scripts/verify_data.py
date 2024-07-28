import pandas as pd
from sqlalchemy import create_engine, text
import logging
import json

# Logging configuration
logging.basicConfig(filename='verify_data.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Configurations
config_path = 'config.json'
csv_path = 'Walmart_cleaned.csv'

# Load configuration from JSON file
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

username = config['username']
password = config['password']
host = config['host']
database = config['database']
table_name = config['table_name']

cleaned_data_path = csv_path

DATABASE_URI = f'mysql+pymysql://{username}:{password}@{host}/{database}'

try:
    # Create the database engine
    engine = create_engine(DATABASE_URI)
    logging.info("Database engine created")

    # Load data from the database
    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        row_count = result.fetchone()[0]
        logging.info("Row count in table %s: %d", table_name, row_count)
        print(f"Row count in table {table_name}: {row_count}")

    # Compare with the original CSV file
    df_csv = pd.read_csv(cleaned_data_path)
    csv_row_count = len(df_csv)
    logging.info("Row count in CSV file: %d", csv_row_count)
    print(f"Row count in CSV file: {csv_row_count}")

    if row_count == csv_row_count:
        logging.info("Row count in the database matches the row count in the CSV file.")
        print("Row count in the database matches the row count in the CSV file.")
    else:
        logging.warning("Row count in the database differs from the row count in the CSV file.")
        print("Warning: Row count in the database differs from the row count in the CSV file.")

    # Verify a random subset of data
    sample_size = min(10, csv_row_count)  # Choose a random subset with a maximum size of 10
    df_sample = df_csv.sample(n=sample_size, random_state=42)

    with engine.connect() as connection:
        for idx, row_csv in df_sample.iterrows():
            result = connection.execute(text(f"SELECT * FROM {table_name} WHERE User_ID={row_csv['User_ID']} AND Product_ID='{row_csv['Product_ID']}' AND Purchase={row_csv['Purchase']}"))
            row_db = result.fetchone()

            logging.info("Row %d from CSV:\n%s", idx, row_csv)
            logging.info("Corresponding row from the database:\n%s", row_db)
            print(f"Row {idx} from CSV:")
            print(row_csv)
            print("Corresponding row from the database:")
            print(row_db)
            print()

    # Visual inspection
    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT * FROM {table_name} LIMIT 5"))
        rows = result.fetchall()

        logging.info("First 5 rows from the database:")
        print("First 5 rows from the database:")
        for row in rows:
            logging.info("%s", row)
            print(row)

except Exception as e:
    logging.error("An error occurred: %s", e)
    print(f"An error occurred: {e}")
