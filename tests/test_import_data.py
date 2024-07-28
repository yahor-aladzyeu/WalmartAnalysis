import unittest
import import_data
import json
import os

class TestImportData(unittest.TestCase):
    def test_import_function(self):
        # Load the configuration from the config.json file
        config_path = 'config.json'
        config = import_data.load_config(config_path)

        # Create a mock CSV file for testing
        with open('test_file.csv', 'w') as csv_file:
            csv_file.write("column1,column2\n1,2\n3,4")

        # Call the import_data function and handle any exceptions
        try:
            import_data.import_data('test_file.csv', config)
        except Exception as e:
            self.fail(f"import_data raised an exception: {e}")

        # Clean up the mock CSV file after testing
        os.remove('test_file.csv')

if __name__ == '__main__':
    unittest.main()
