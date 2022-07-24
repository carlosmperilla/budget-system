import unittest, os
from pre_requirements import BASE_FOLDER
from budget_system import Spent
from budget_system.settings.Config import ConfigBudget
from pandas.core.frame import DataFrame
from numpy import float64

class SpentTest(unittest.TestCase):
    
    def setUp(self) -> None:
        os.environ['CONFIG_BUDGET'] = os.path.join(BASE_FOLDER, 'config.ini')
        self.year = 2022
        self.month = 'May'
        self.store_name = 'storeone'
        self.date = '15-05-22'
        self.d_index = 0 #dict index

    def test_get_productsdata_concrete(self):
        month_path = ConfigBudget().MONTH_PATH.format(year=self.year, month=self.month)
        products_data = Spent().spending_by_sector_in_month(month_path, self.store_name)[self.d_index][self.store_name][self.date]

        least_expensive, most_expensive, spent = products_data
        self.assertEqual(type(least_expensive), DataFrame)
        self.assertEqual(type(most_expensive), DataFrame)
        self.assertEqual(type(spent), float64)

    def test_get_productsdata_full(self):
        products_data = Spent().total_spending()[self.d_index][self.year][self.d_index][self.month][self.d_index][self.store_name][self.date]

        least_expensive, most_expensive, spent = products_data
        self.assertEqual(type(least_expensive), DataFrame)
        self.assertEqual(type(most_expensive), DataFrame)
        self.assertEqual(type(spent), float64)

    def test_get_datesdict_concrete(self):
        month_path = ConfigBudget().MONTH_PATH.format(year=self.year, month=self.month)
        dates_dict = Spent().spending_by_sector_in_month(month_path, self.store_name)[self.d_index][self.store_name]

        for date in dates_dict:
            self.assertEqual(len(date.split('-')), 3)
            self.assertEqual(type(dates_dict[date]), tuple)

    def test_get_datesdict_full(self):
        dates_dict = Spent().total_spending()[self.d_index][self.year][self.d_index][self.month][self.d_index][self.store_name]
        
        for date in dates_dict:
            self.assertEqual(len(date.split('-')), 3)
            self.assertEqual(type(dates_dict[date]), tuple)

    def test_get_sectorsdict_concrete(self):
        month_path = ConfigBudget().MONTH_PATH.format(year=self.year, month=self.month)
        sectors_dict = Spent().spending_by_sector_in_month(month_path, self.store_name)[self.d_index]

        for sector in sectors_dict:
            self.assertEqual(type(sectors_dict[sector]), dict)

    def test_get_sectorsdict_full(self):
        sectors_dict = Spent().total_spending()[self.d_index][self.year][self.d_index][self.month][self.d_index]
        
        for sector in sectors_dict:
            self.assertEqual(type(sectors_dict[sector]), dict)

    def test_get_monthdata_exact(self):
        month_data = Spent().spending_by_month(self.year, self.month)

        month_content, month_spent = month_data 

        self.assertEqual(type(month_spent), float64)
        self.assertEqual(type(month_content), dict)

    def test_get_monthdata_full(self):
        month_data = Spent().total_spending()[self.d_index][self.year][self.d_index][self.month]

        month_content, month_spent = month_data 

        self.assertEqual(type(month_spent), float64)
        self.assertEqual(type(month_content), dict)

    def test_get_monthdata_one_store_in_a_month_exact(self):
        month_path = ConfigBudget().MONTH_PATH.format(year=self.year, month=self.month)
        month_data = Spent().spending_by_sector_in_month(month_path, self.store_name)

        month_content, month_spent = month_data 

        self.assertEqual(type(month_spent), float64)
        self.assertEqual(type(month_content), dict)

    def test_get_yeardata_exact(self):
        year_data = Spent().spending_by_year(self.year)

        year_content, year_spent = year_data 

        self.assertEqual(type(year_spent), float64)
        self.assertEqual(type(year_content), dict)

    def test_get_yeardata_full(self):
        year_data = Spent().total_spending()[self.d_index][self.year]

        year_content, year_spent = year_data 

        self.assertEqual(type(year_spent), float64)
        self.assertEqual(type(year_content), dict)

    def test_get_totaldata(self):
        total_data = Spent().total_spending()

        total_content, total_spent = total_data 

        self.assertEqual(type(total_spent), float64)
        self.assertEqual(type(total_content), dict)


if __name__ == '__main__':
    unittest.main(verbosity=2)