"""This module handles date validations."""
#To access the configuration file
import configparser

#For data types.
from typing import List, Dict

#To get the current path
import pathlib
#To join paths
import os.path
#Read and write month data
import shelve

#This gets the default language.
from ..settings.Lang import LANG

#Text for errors.
from ..settings.LanguagesText import get_month_text

#Get the current path
current_path = pathlib.Path(__file__).parent.absolute()
#Path with the information of the months by language
month_data_path = os.path.join(current_path, 'months', "months_by_lang")

def import_months_by_lang(lang:str, months:List[str]) -> None:
    """With the language key and a list of months arranged in that language, 
    you can save it for future uses in the application. 
    Or a new folder format in that language.
    """
    with shelve.open(month_data_path) as month_file:
        month_file[lang] = (months[0]!="")*[""]+months

def get_months_dict() -> Dict[str, List[str]]:
    """This gets a dictionary with the language keys as the key
    and the list of months as the value.
    """
    with shelve.open(month_data_path) as month_file:
        dict_month = dict(month_file)
    return dict_month

class Month:
    """"""

    class MonthNotValid(Exception):
        """The month is not valid. It is not by default, 
        a list of compatible months has not been imported 
        """
        pass

    class MonthEmpty(Exception):
        """The month is empty."""
        pass

    @staticmethod
    def __is_empty(month:str) -> bool:
        """Check if the month is empty."""
        return (month == "")

    @staticmethod
    def get_months(lang:str=LANG) -> List[str]:
        """Get the months in a particular language."""
        lang_=lang
        if os.environ.get('CONFIG_BUDGET'):
            config = configparser.ConfigParser()
            config.read(os.environ["CONFIG_BUDGET"], encoding="utf-8")
            lang_ = config["DEFAULT"]["lang"]
        months = get_months_dict().get(lang_)
        return months

    def __init__(self) -> None:
        self.message_MonthNotValid,\
        self.message_MonthEmpty = get_month_text()

    def __error_empty(self) -> None:
        """Raise an error in case the month is empty."""
        raise self.MonthEmpty(self.message_MonthEmpty)

    def __error_valid(self) -> None:
        """Raise an error in case the month is not valid."""
        raise self.MonthNotValid(self.message_MonthNotValid)

    def get_month_by_index(self, index:int, lang:str=LANG) -> str:
        """This gets the month by its index."""
        return self.get_months(lang)[index]

    def __in_months(self, month:str) -> None:
        """Check if the month is in months."""
        return (month in self.get_months())

    def validate(self, month:str) -> str:
        """This checks that the month is valid."""


        in_months = self.__in_months(month)
        is_empty = self.__is_empty(month)

        if not in_months:
            self.__error_valid()

        if is_empty:
            self.__error_empty()

        return month
