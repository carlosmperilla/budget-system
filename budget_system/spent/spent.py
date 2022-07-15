"""This module manages the branched visualization of spent
Total >> Year >> Month >> Sector >> Date
"""

#To list the directories
import os

#Type of data.
from numpy import float64
from typing import Dict, List, Union
from ..extra_types.SpentTypes import ProductsData, DatesDict, MonthData, YearData, TotalData

#To verify that the month is valid
from ..validators.Date import Month

#This allows us to obtain the configuration of budgets
from ..settings.Config import ConfigBudget

#To handle the purchase table
from ..purchase import PurchaseList
#To extract data from the table name.
from ..parsers import ParserTableName

class Spent:
    """Class that is responsible for the extraction and management of data by month, year and total.
    Note: If you want expenses by sector-date, use the PurchaseList class.
    """

    @staticmethod
    def sum_of_expenses(periods: Union[Dict[str, MonthData] , Dict[str, YearData]]) -> float64:
        """Gets the spent by total or by year."""
        return sum(spent_by_period[1] for spent_by_period in periods.values())

    def __init__(self) -> None:
        #When instantiating we verify that the config.ini path exists in the environment variables
        self.__config_budget = ConfigBudget()

        self.CONFIG_FILE_NAME = self.__config_budget.CONFIG_FILE_NAME
        self.BASE_PATH,\
        self.YEAR_PATH,\
        self.MONTH_PATH,\
        self.TABLE_PATH = self.__config_budget.get_paths()


        #Index with the spent in the product data
        self.spending_index = 2

    def extract_month_data(self, purchase_lists:List[str], month_path:str) -> MonthData:
        """Generates a tuple with the sectors per month, and the total spent of the month.
        Note: You can pass a list filtered by sector and the path of the month, to get the spents made by store.
        """
        sectors_by_month = {}
        total_spent_month = float64(0)
        for table_name in purchase_lists:
            #This generates the Purchase List from the file in the month folder to work with its data
            location_csv = self.TABLE_PATH.format(month_path=month_path, table_name=table_name)
            table_purchase = PurchaseList(location_csv)

            #Store name and date of purchase
            store_name, table_date = ParserTableName(table_name).get_all()

            #If the sector key does not exist, it creates it and gives it an empty dictionary value. 
            # If the key exists, we store the dictionary it contains, to fill it with dates.
            date_data : DatesDict = sectors_by_month.setdefault(store_name, {})
            #This fills the sector date, with the product data.
            products_data : ProductsData = date_data.setdefault(table_date, table_purchase.get_all())
            #This stores the cost per month
            total_spent_month += products_data[self.spending_index]

        return (sectors_by_month, total_spent_month)

    def spending_by_sector_in_month(self, month_path:str, store:str) -> MonthData:
        """This returns the spent per store in a specific month,
        with information on each of its spending dates
        """
        filtered_purchase_lists = [
            table
                for table in os.listdir(month_path)
                    if store in table
        ]
        return self.extract_month_data(filtered_purchase_lists, month_path)

    def spending_by_month(self, year:int, month:str) -> MonthData:
        """This returns the spent per month and inherited spent information."""
        
        #This validates the month
        valid_month = Month().validate(month)

        #This generates the path of the month
        month_path = self.MONTH_PATH.format(year=year, month=valid_month)
        #This lists the tables with the purchases made by sector and date.
        purchase_lists = os.listdir(month_path)

        return self.extract_month_data(purchase_lists, month_path)

    def spending_by_year(self, year:int) -> YearData:
        """This returns the spent per year and inherited spent information."""
        
        #This lists the months by year.
        #And it generates the path of the year
        months_by_year = os.listdir(self.YEAR_PATH.format(year=year))

        #Data of the months per year
        months_data = {
            month : self.spending_by_month(year, month)
                for month in months_by_year
            }
        
        #Sum of expenses per year.
        year_spent = self.sum_of_expenses(months_data)

        return (months_data, year_spent)

    def total_spending(self) -> TotalData:
        """This returns the total spent and inherited spent information."""

        #This lists the years in the budget
        years = (
            int(year_str) 
                for year_str in os.listdir(self.BASE_PATH) 
                    if year_str != self.CONFIG_FILE_NAME
                    )

        #Data of the years
        years_data = {
            year : self.spending_by_year(year)
                for year in years
            }

        #Total spent in budget.
        total_spent = self.sum_of_expenses(years_data)

        return (years_data, total_spent)
