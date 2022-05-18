"""This module is responsible for the aesthetic display of data by shell."""

#For the type of data to display
from typing import Union, Dict, Callable

#To sort the dates by sector.
from datetime import datetime

#To support and start ANSI coloring of the shell
from colorama import init

#Types managed in spents
from ..extra_types.SpentTypes import DatesDict, SectorsDict, MonthData, YearData, TotalData

#Shell print styles
from ..settings.DisplayStyle import (
                      WIDTH_CHR,
                      STYLE_SEPARATOR, 
                      STYLE_DATE,
                      STYLE_SPENT_TITLE,
                      STYLE_SPENT_TOTAL_TITLE,
                      STYLE_SPENT_YEAR_TITLE,
                      STYLE_SPENT_MONTH_TITLE,
                      STYLE_SECTOR_TITLE,
                      STYLE_LEAST_EXPENSIVE_TITLE,
                      STYLE_MOST_EXPENSIVE_TITLE
                      )

#To sort the dates by sector.
from ..settings.DateFormat import DATE_FORMAT

#Text to display by language
from ..settings.LanguagesText import get_show_data_text

#To sort the months by year
from ..validators.Date import Month

#To get the data of the spent
from ..spent import Spent

def separator(pos="BEGIN"):
    """Decorator that places a separator at the beginning or end of a block."""
    
    sep_desing = STYLE_SEPARATOR+"*_"*(WIDTH_CHR//2)+"*\n"
    
    def custom_separator(function):
        def wrapper(*args, **kwargs):
    
            if pos == "BEGIN":
                print(sep_desing)
    
            result = function(*args, **kwargs)
    
            if pos == "END":
                print(sep_desing)
    
            return result
    
        return wrapper
    
    return custom_separator


class DisplayData:
    """Displays the data information on the screen.
    Total, by year, by month, by sector and by date."""

    @staticmethod
    def iter_sorted_dict(
            dictionary:dict, 
            sort_function:Callable, 
            function:Callable[[Union[str, int], dict], None]
        ):
        """This sort the dictionary and iterate over a function
        with its keys and the dictionary itself."""

        dictionary_sort = sorted(dictionary, key=sort_function)
        for key in dictionary_sort:
            function(key, dictionary)

    def __init__(self) -> None:
        init(autoreset=True) #Se resetean los colores.
        self.message_TotalSpent,\
        self.message_YearSpent,\
        self.message_MonthSpent,\
        self.message_DateSpent,\
        self.message_LeastExpensive,\
        self.message_MostExpensive = get_show_data_text()
           
    def auxiliar_show(
            self,
            n_tab:int,
            title:str, 
            style, 
            data:tuple,
            function:Callable[[Union[str, int], dict], None],
            sort_function:Callable=None
        ):
        """General display function. 
        n_tab: regular amount of tabs.
        title: Text to display in the title.
        style: For the title.
        data: Tuple with a dictionary and an spent respectively.
        function: this displays information, with a dictionary key and the dictionary.

        Optional: A sort function, to display the data in a specific order.
        """
        print("\t"*n_tab+style+title)
        print("\t"*(n_tab+1)+str(data[1])+"\n")

        dictionary = data[0]
        self.iter_sorted_dict(dictionary, sort_function, function)  

    def show_date_data(self, buy_date:str, data_buy_dates:DatesDict)->None:
        """This shows the information of spent in the date by sector.
        The cheapest and the most expensive products.
        """
        n_tab = 3
        print('\n'+'\t'*n_tab+STYLE_DATE+f"{buy_date}")
        print('\t'*n_tab+STYLE_SPENT_TITLE+self.message_DateSpent)
        #Spent by date.
        print('\t'*(n_tab+1)+f"{data_buy_dates[buy_date][2]}\n")
        
        print(STYLE_LEAST_EXPENSIVE_TITLE+self.message_LeastExpensive.center(WIDTH_CHR, '-'))
        #The cheapest products.
        print(data_buy_dates[buy_date][0])
        print("\n")
        print(STYLE_MOST_EXPENSIVE_TITLE+self.message_MostExpensive.center(WIDTH_CHR, '-'))
        #The most expensive products.
        print(data_buy_dates[buy_date][1])
        print("\n")

    def show_sector_data(self, store:str, data_stores:SectorsDict) -> None:
        """This shows the information of spent in the sector"""
        print(STYLE_SECTOR_TITLE+f"{store}".center(WIDTH_CHR))

        data_buy_dates = data_stores[store]
        #This sorts the dates by sector
        sort_function = lambda date: datetime.strptime(date, DATE_FORMAT)
        self.iter_sorted_dict(data_buy_dates, sort_function, self.show_date_data)
    
    @separator(pos="BEGIN")
    def show_month_data(self, month:str, data_months: Dict[str, MonthData]) -> None:
        """This shows the information of spent in the month"""
        self.auxiliar_show(
                2, 
                self.message_MonthSpent.format(month=month), 
                STYLE_SPENT_MONTH_TITLE, 
                data_months[month], 
                self.show_sector_data
            )
    
    @separator(pos="END")
    def show_year_data(self, year:int, data_years: Dict[int, YearData]) -> None:
        """This shows the information of spent in the year."""
        #This sorts the months.
        sort_function = Month().get_months().index
        self.auxiliar_show(
                1, 
                self.message_YearSpent.format(year=year), 
                STYLE_SPENT_YEAR_TITLE, 
                data_years[year], 
                self.show_month_data,
                sort_function
            )
 
    def show_total_data(self) -> None:
        """Show all spent information."""
        print("\n")
        data_spent:TotalData = Spent().total_spending() #Se extraen todos los datos de gastos
        self.auxiliar_show(
                0, 
                self.message_TotalSpent, 
                STYLE_SPENT_TOTAL_TITLE, 
                data_spent, 
                self.show_year_data
            )

if __name__ == "__main__":
    DisplayData().show_total_data()
