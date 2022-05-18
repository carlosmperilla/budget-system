"""This module is responsible for managing the creation and updating of the budget system."""

#To join paths, list, create and rename directories.
import os
#To move and copy
import shutil
#To manage the configuration file.
import configparser
#To get month number and year from table name
from datetime import datetime
#To type data.
from typing import List, Dict, Tuple, Set, Callable

#To handle the default language
from .settings.Lang import LANG
#Date format.
from .settings.DateFormat import DATE_FORMAT

#This gets the month in your language by index.
from .validators.Date import Month
#To get store name and date.
from .parsers import ParserTableName
#To get the error messages.
from .settings.LanguagesText import get_budget_system_text


class Budget:
    """This class is responsible for managing the creation and updating of the budget system.
    So it must be the first to be used.
    """
    
    class FolderTreeDoesntExist(Exception):
        """The directory tree has not been created or identified."""
        pass

    @staticmethod
    def translate_month_folders(config_file_path:str, current_lang:str, new_lang:str) -> None:
        """This translates the months into the budget system.
        Example:
            translate_month_folders(CONFIG_PATH, "ENG", "SPA")
        Note:
            If the language is not available, you can import the months with 'import_months_by_lang'
            And generate the texts with 'generate_lang_texts'
        """
        
        def get_config(config_file_path:str) -> configparser.ConfigParser:
            """This reads the config file."""
            config = configparser.ConfigParser()
            config.read(config_file_path, encoding="utf-8")
            return config
        
        def get_base_path(config:configparser.ConfigParser) -> str:
            """This gets the base directory"""
            return config["DEFAULT"]["base_path"]

        def is_folder(folder:str) -> bool:
            """This checks if it is a directory."""
            return os.path.isdir(folder)

        def translate_month(month:str) -> str:
            """This translates a month into an available language."""
            month_valid = Month()
            month_index = month_valid.get_months(current_lang).index(month)
            translated_month = month_valid.get_months(new_lang)[month_index]
            return translated_month
        
        def translate_month_path(month_path:str) -> str:
            """This outputs the translated month path"""
            year_path, month = os.path.split(month_path)
            translated_month_path = os.path.join(
                                                year_path, 
                                                translate_month(month)
                                                )
            return translated_month_path

        def iter_valid_folders(path:str, function:Callable[[str], None]) -> None:
            """This lists the folders in a directory, from some period, years or months.
            Then checks that they are folders, if they are, runs a function on each of them.
            """
            period_folders = os.listdir(path)
            for period_folder in period_folders:
                period_folder_path = os.path.join(path, period_folder)
                if is_folder(period_folder_path):
                    function(period_folder_path)

        def rename_month(month_path:str) -> None:
            """This renames the folder of the indicated month with its translated version."""
            translated_month_path = translate_month_path(month_path)
            os.rename(month_path, translated_month_path)          

        def iter_month_folders(year_path:str) -> None:
            """This iterates over the month directories of a specific year.
            """
            iter_valid_folders(year_path, rename_month)

        def iter_year_folders(base_path:str) -> None:
            """This iterates over the year directories contained in the base directory.
            """
            iter_valid_folders(base_path, iter_month_folders)

        def change_lang_config(config):
            """This changes the language of the config to that of the translated months.
            """
            config["DEFAULT"]["lang"] = new_lang
            with open(config_file_path, "w", encoding="utf-8") as config_file:
                config.write(config_file)

        config = get_config(config_file_path)
        base_path = get_base_path(config)
        iter_year_folders(base_path)
        change_lang_config(config)

    @staticmethod
    def get_file_name(file_path:str) -> str:
        """This gets the name of a file from its path."""
        file_name = os.path.split(file_path)[1]
        return file_name

    @staticmethod
    def escape_interpolation_config(info):
        """This avoids interpolation problems when exporting the configuration."""
        return info.replace("%", "%%")

    @staticmethod
    def copy_budget_files(current_location, next_location) -> None:
        """This copies a file from your current location to the budget system location.
        """
        shutil.copy(current_location, next_location)

    @staticmethod
    def move_budget_files(current_location, next_location) -> None:
        """This moves a file from your current location to the budget system location.
        """
        shutil.move(current_location, next_location)

    def __init__(
            self, 
            base_folder:str,
            budget_files:List[str],
            lang:str=LANG,
            price_name:str="",
            budget_files_action="COPY",
            date_format:str = DATE_FORMAT
        ) -> None:
        self.base_folder = base_folder        

        self.current_location_budget_files = budget_files
        #This will contain the paths of the current files and their new paths in the budget system.
        self.next_location_budget_files : List[Tuple[str, str]] = []

        self.lang = lang
        self.price_name = price_name
        self.budget_files_action = budget_files_action
        self.date_format = date_format
        
        self.years : Dict[str, Set[str]] = {}
        self.folder_tree_exist : bool = False
        self.message_FolderTreeDoesntExist = get_budget_system_text()[0]

    def get_new_location(self, year:str, month:str, budget_file_name:str="") -> str:
        """This generates the new path of a file in the budget system."""
        new_location = os.path.join(self.base_folder, str(year), month, budget_file_name)
        return new_location

    def get_month_and_year(self, budget_file_name : str) -> Tuple[str, str]:
        """This gets the month and year from a table."""
        date_text = ParserTableName(budget_file_name).get_table_date()
        date = datetime.strptime(date_text, self.date_format)
        
        year, month = date.year, Month().get_month_by_index(date.month, self.lang)
        return (year, month)

    def add_month_to_year(self, year:str, month:str) -> None:
        """This generates one set per year that the months adhere to."""
        self.years.setdefault(year, set())
        self.years[year].add(month)

    def fill_move_locations(self) -> None:
        """This populates the current file paths and your new paths in the budget system.
        To move the files or copy them.
        """
        for budget_file_path in self.current_location_budget_files:
            budget_file_name =  self.get_file_name(budget_file_path)
            year, month = self.get_month_and_year(budget_file_name)
            new_location = self.get_new_location(year, month, budget_file_name)

            self.add_month_to_year(year, month)

            self.next_location_budget_files.append((budget_file_path, new_location))

    def folder_tree_genearator(self) -> bool:
        """If the directory tree to create does not exist, it generates it.
        Either to create the budget system or to add new budget-files.
        """
        if not self.folder_tree_exist:
            for year, months in self.years.items():
                for month in months:
                    os.makedirs(self.get_new_location(year, month), exist_ok=True)
            self.folder_tree_exist = True
        return self.folder_tree_exist

    def action(self) -> None:
        """If the directory tree exists, copy or move the files."""
        if self.folder_tree_exist:
            for current_location, next_location in self.next_location_budget_files:
                {
                    "COPY" : self.copy_budget_files,
                    "MOVE" : self.move_budget_files
                }.get(self.budget_files_action)(current_location, next_location)
        else:
            raise self.FolderTreeDoesntExist(self.message_FolderTreeDoesntExist)
    
    def create_config_file(self) -> None:
        """If the directory tree exists, it generates the configuration file."""
        if self.folder_tree_exist:
            config = configparser.ConfigParser()
            config['DEFAULT'] = {
                'lang' : self.lang,
                'price_name' : self.price_name,
                'date_format' : self.escape_interpolation_config(self.date_format),
                'base_path' : self.base_folder,
            }
            
            config_file_path = os.path.join(self.base_folder, 'config.ini')
            
            with open(config_file_path, 'w', encoding="utf-8") as configfile:
                config.write(configfile)
        else:
            raise self.FolderTreeDoesntExist(self.message_FolderTreeDoesntExist)

    def add_budget_files(self):
        """This adds files to the budget system, if it does not exist, create it.
        Note: To create the budget system with its configuration file use 'create_budget_system' instead
        """
        self.fill_move_locations()
        self.folder_tree_genearator()
        self.action()

    def create_budget_system(self):
        """This creates the budget system."""
        self.add_budget_files()
        self.create_config_file()
