"""This module is responsible for reading the tables and processing them in order to use their data.
The use of pandas or any other parsing of the particular data table should be done here.
"""

#To read and analyze the data tables
import pandas as pd

#Types for the tables
from pandas.core.frame import DataFrame
from numpy import float64

#Type for the products
from ..extra_types.SpentTypes import ProductsData

#To get the name of the column with the prices
from ..settings.Config import ConfigBudget

class PurchaseList:
    """Class that reads the table with the purchases,
    sorts them by price and extracts the relevant data.
    """

    def __init__(self, location:str) -> None:
        #Name of the column with the prices.
        self.price_name: str = ConfigBudget().PRICE_NAME

        self.data_frame =  pd.read_csv(location, delimiter=",")
        self.df_by_price = self.data_frame.sort_values(self.price_name) #This sorts by price.

    def most_expensive(self, n:int=3) -> DataFrame:
        """This gets the most expensive products."""
        return self.df_by_price.tail(n)

    def least_expensive(self, n:int=3) -> DataFrame:
        """This gets the most least products."""
        return self.df_by_price.head(n)

    def spending_by_sector(self) -> float64:
        """This calculates the total spending.
        This calculates the total expense.
        Remember that each table corresponds to a date in a store.
        """
        return self.df_by_price[self.price_name].sum()

    def get_all(self) -> ProductsData:
        """Returns the important data for data sampling.
        This is the basic unit of data sampling.
        """
        
        low_cost = self.least_expensive()
        hight_cost = self.most_expensive()
        total_spent = self.spending_by_sector()
        
        return (low_cost, hight_cost, total_spent)