import unittest
from pre_requirements import (
        BASE_FOLDER,
        test_tables_csv_folder_name,
        generate_test_tables, 
        remove_test_tables
        )
from budget_system import Budget
import os

class CreationAndAdditionTest(unittest.TestCase):

    def setUp(self) -> None:
        generate_test_tables()
        self.budget_files = [os.path.join(test_tables_csv_folder_name, table_name) for table_name in os.listdir(test_tables_csv_folder_name)]
        self.base_folder = BASE_FOLDER
        self.context = {
            "lang" : "ENG",
            "price_name" : "Price",
            "base_folder" : self.base_folder,
            "budget_files" : self.budget_files[:2],
            "budget_files_action" : "COPY",
            "date_format" : "%d-%m-%y"
        }
        self.budget = Budget(**self.context)

    def test_creating_a_Budget_System(self):
        self.budget.create_budget_system()

    def test_exist_Budget_System_Config(self):
        config_budget_path = os.path.join(self.base_folder, 'config.ini') 
        self.assertTrue(os.path.isfile(config_budget_path))

    def test_addition_files(self):
        addition_files = self.budget_files[2:]
        self.context["budget_files"] = addition_files

        budget = Budget(**self.context)
        budget.add_budget_files()

    def tearDown(self) -> None:
        remove_test_tables()

if __name__ == '__main__':
    unittest.main(verbosity=2)