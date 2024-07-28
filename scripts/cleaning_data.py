import pandas as pd

def clean_data(data):
    # Remove rows with missing values
    data = data.dropna()

    # Define categorical columns
    cat_columns = ['Gender', 'Age', 'Occupation', 'City_Category',
                           'Stay_In_Current_City_Years', 'Marital_Status',
                           'Product_Category']

    # Convert categorical columns to 'category' dtype
    data[cat_columns] = data[cat_columns].astype('category')

    # Define numerical columns to convert to numeric dtype
    num_columns = ['User_ID', 'Purchase']

    # Convert numerical columns to numeric dtype
    data[num_columns] = data[num_columns].apply(pd.to_numeric, errors='coerce')

    # Remove duplicates
    data = data.drop_duplicates()

    # Reset index
    data = data.reset_index(drop=True)

    return data

def clean_data_file(file_path):
    try:
        # Load data from file
        dt = pd.read_csv(file_path)

        # Clean the data using the clean_data function
        cleaned_dt = clean_data(dt)

        # Save cleaned data to a new CSV file
        cleaned_file_path = "Walmart_cleaned.csv"
        cleaned_dt.to_csv(cleaned_file_path, index=False)

        print(f"Data cleaned and saved to {cleaned_file_path}")
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file {file_path} is empty.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Load and clean data from'Walmart.csv'
clean_data_file('Walmart.csv')

