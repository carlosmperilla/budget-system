"""This module has the classes to parse strings."""

#For the type of get_all
from typing import Tuple

class ParserTableName():
    """Class to parse and extract data from table name
    
    Name format:
        whatever_StoreName_[Date].csv
    
    Example:
        For a shopping list of May 23, 2022:
            'shopping_list_Drugstore_[23-05-22].csv'
    """

    def __init__(self, table_name:str) -> None:
        self.table_name = table_name

    def get_store_name(self) -> str:
        """Split the table name into a list, using '_' as delimiter,
        get the second string from tail to head
        """
        
        return self.table_name.split('_')[-2]

    def get_table_date(self) -> str:
        """Split the table name into a list, using '[' as delimiter,
        get the first string from tail to head,
        and cuts the last 5 characters.
        """

        table_date = self.table_name.split('[')[-1][:-5]
        return table_date

    def get_all(self) -> Tuple[str, str]:
        """Returns the important parsed table name information.
        """

        store_name = self.get_store_name()
        table_date = self.get_table_date()
        
        return (store_name, table_date)