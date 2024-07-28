import unittest
import pandas as pd
from io import StringIO
from cleaning_data import clean_data


class TestCleanData(unittest.TestCase):

    def setUp(self):
        # Sample data for use in tests
        self.sample_data = StringIO("""User_ID,Product_ID,Gender,Age,Occupation,City_Category,Stay_In_Current_City_Years,Marital_Status,Product_Category,Purchase
1000001,P00069042,F,0-17,10,A,2,0,3,8370
1000002,P00248942,M,55+,16,C,4+,0,1,15200
1000003,P00087842,M,26-35,15,A,3,0,12,1422
1000004,P00085442,M,46-50,7,B,2,1,8,1057
1000005,P00285442,M,46-50,7,B,2,1,1,7969
1000006,P00193542,F,26-35,1,B,1,0,1,15227
1000007,P00184942,M,46-50,7,B,2,1,1,19215
1000008,P00274942,F,36-45,2,B,1,1,1,15854
1000009,P00251242,M,26-35,17,C,2,0,5,15686
1000010,P00037642,M,36-45,1,B,1,1,1,7871
""")

    def test_clean_data(self):
        # Load sample data into a DataFrame
        data = pd.read_csv(self.sample_data)

        # Perform the cleaning process
        cleaned_data = clean_data(data)

        # Test that missing values are dropped
        self.assertFalse(cleaned_data.isnull().values.any(), "Dane zawierają brakujące wartości.")

        # Test that categorical columns are of type 'category'
        categorical_columns = ['Gender', 'Age', 'Occupation', 'City_Category', 'Stay_In_Current_City_Years',
                               'Marital_Status', 'Product_Category']
        for col in categorical_columns:
            self.assertEqual(cleaned_data[col].dtype.name, 'category', f"Kolumna {col} nie jest typu 'category'.")

        # Test that numerical columns are of type 'int64'
        self.assertEqual(cleaned_data['User_ID'].dtype, 'int64', "Kolumna 'User_ID' nie jest typu 'int64'.")
        self.assertEqual(cleaned_data['Purchase'].dtype, 'int64', "Kolumna 'Purchase' nie jest typu 'int64'.")

        # Test that there are no duplicates
        self.assertEqual(cleaned_data.duplicated().sum(), 0, "Dane zawierają zduplikowane wiersze.")

        # Test that the index is reset
        self.assertTrue((cleaned_data.index == range(len(cleaned_data))).all(),
                        "Indeks nie został poprawnie zresetowany.")


if __name__ == '__main__':
    unittest.main()
