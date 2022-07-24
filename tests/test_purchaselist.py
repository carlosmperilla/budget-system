import unittest, os
from pre_requirements import BASE_FOLDER
from budget_system import PurchaseList
from budget_system.settings.Config import ConfigBudget
from pandas.core.frame import DataFrame
from numpy import float64

class PurchaseListTest(unittest.TestCase):
    
    def setUp(self) -> None:
        os.environ['CONFIG_BUDGET'] = os.path.join(BASE_FOLDER, 'config.ini')
        self.year, self.month = 2022, 'May'
        self.month_path = ConfigBudget().MONTH_PATH.format(year=self.year, month=self.month)
        self.file_name = 'test_table_one_storeone_[15-05-22].csv'
        self.location = os.path.join(self.month_path, self.file_name)

    def test_get_productsdata(self):
        products_data = PurchaseList(self.location).get_all()

        least_expensive, most_expensive, spent = products_data
        self.assertEqual(type(least_expensive), DataFrame)
        self.assertEqual(type(most_expensive), DataFrame)
        self.assertEqual(type(spent), float64)

    def test_get_n_most_expensive_products(self):
        n_products = 5
        most_expensive = PurchaseList(self.location).most_expensive(n_products)

        self.assertEqual(type(most_expensive), DataFrame)

    def test_get_n_least_expensive_products(self):
        n_products = 5
        least_expensive = PurchaseList(self.location).least_expensive(n_products)

        self.assertEqual(type(least_expensive), DataFrame)

    def test_get_total_spent(self):
        spent_by_table = PurchaseList(self.location).spending_by_sector()

        self.assertEqual(type(spent_by_table), float64)

    def test_get_full_dataframe(self):
        df = PurchaseList(self.location).data_frame
        self.assertEqual(type(df), DataFrame)

    def test_get_full_dataframe_sorted_by_price(self):
        df_by_price = PurchaseList(self.location).df_by_price
        self.assertEqual(type(df_by_price), DataFrame)


if __name__ == '__main__':
    unittest.main(verbosity=2)