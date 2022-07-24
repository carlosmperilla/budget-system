import unittest, os
from pre_requirements import BASE_FOLDER
from budget_system import DisplayData, Spent
from budget_system.settings.Config import ConfigBudget

class VisualizationTest(unittest.TestCase):

    def setUp(self) -> None:
        os.environ['CONFIG_BUDGET'] = os.path.join(BASE_FOLDER, 'config.ini')

    def test_display_total_data(self):
        DisplayData().show_total_data()

    def test_display_year_data(self):
        year = 2022
        data_years = Spent().spending_by_year(year)
        year_data_by_key = {year:data_years}
        DisplayData().show_year_data(year, year_data_by_key)

    def test_display_month_data(self):
        year, month = 2022, 'May'
        data_months = Spent().spending_by_month(year, month)
        month_data_by_key = {month : data_months}

        DisplayData().show_month_data(month, month_data_by_key)

    def test_display_store_data(self):
        year, month, store_name = 2022, 'May', 'storeone'
        month_path = ConfigBudget().MONTH_PATH.format(year=year, month=month)
        sector_data_by_key = Spent().spending_by_sector_in_month(month_path, store_name)[0]
        DisplayData().show_sector_data(store_name, sector_data_by_key)

    def test_display_date_sectordate_data(self):
        year, month, store_name, buy_date = 2022, 'May', 'storeone', '15-05-22'
        month_path = ConfigBudget().MONTH_PATH.format(year=year, month=month)
        sector_data_by_key = Spent().spending_by_sector_in_month(month_path, store_name)[0]
        date_data_by_key = {buy_date : sector_data_by_key[store_name][buy_date]}
        DisplayData().show_date_data(buy_date, date_data_by_key)

if __name__ == '__main__':
    unittest.main(verbosity=2)
