import os, shutil, configparser, csv
from pathlib import Path

BASE_FOLDER = r"MyTestBudget"

default_column_names = ['Name', 'Brand', 'Amount', 'Price']
test_tables_info_folder_name = 'test_tables_information'
test_tables_csv_folder_name = 'test_tables_csv'


def generate_test_tables() -> None:
    """
        Generates the .csv tables necessary to test the Budget System.
    """
    
    def read_config_file(test_table : str) -> configparser.ConfigParser:
        """
            Reads the file with the information of a test table from the folder of predefined tests.
        """
        config = configparser.ConfigParser()
        test_table_path = Path().joinpath(test_tables_info_folder_name, test_table)
        config.read(test_table_path)
        return config

    def get_rows(config : configparser.ConfigParser) -> list:
        """
            Create a list of lists, each list represents a row.
        """
        return [
                    default_column_names, 
                    ] + [
                            dict(config[product_info]).values() 
                                for product_info in config.sections()
                                ]

    def writing_rows(test_table_csv : str, rows : list) -> None:
        """
            Write the rows to csv files.
        """
        os.makedirs(test_tables_csv_folder_name, exist_ok=True)
        with open(Path().joinpath(test_tables_csv_folder_name, test_table_csv), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    for test_table in os.listdir(test_tables_info_folder_name):
        
        config = read_config_file(test_table)
        test_table_csv = Path(test_table).stem + '.csv'
        rows = get_rows(config)

        writing_rows(test_table_csv, rows)

def remove_test_tables() -> None:
    """
        Remove the test CSV folder.
    """

    shutil.rmtree(test_tables_csv_folder_name)