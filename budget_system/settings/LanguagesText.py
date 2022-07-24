"""This module controls the management of texts to be displayed in the application. 
Errors, messages and labels
"""

#For the typing of the generate_lang_texts
from typing import Dict, Tuple

#To get the current file path
import pathlib
#To join routes
import os.path

#To read and write the configuration file texts
import configparser

#Get the current language
from .Lang import LANG

#Get the current path
current_path = pathlib.Path(__file__).parent.absolute()

def generate_lang_texts(lang:str, sections:Dict[str, Dict[str, str]]) -> configparser.ConfigParser:
    """This generates a {LANG}.ini file with the necessary texts to work in languages other than the default ones.
     Or to overwrite message texts for the current setting.
     """

    lang_ini_path = os.path.join(current_path, f"languages/{lang}.ini")
    config = configparser.ConfigParser()
    path_exist = os.path.exists(lang_ini_path)
    
    #Get the previous text configuration
    if path_exist:
        config.read(lang_ini_path, encoding="utf-8")

    for section, messages in sections.items():
        #If the path already exists, it overwrites the fields one by one.
        if path_exist:
            for label in messages:
                config[section][label] = messages[label]
        else:
            #Otherwise it overwrites each section.
            config[section] = messages

    #Save or generate the language file
    with open(lang_ini_path, "w", encoding="utf-8") as lang_file:
        config.write(lang_file)

    #This returns a value with the configuration in case you want a backup.
    return config

class Language:
    """Class that contains the basic texts of each configuration,
    based on the default language in the app.
    """
    
    class Month:
        def __init__(self):
            self.message_MonthNotValid = config["Month"]["message_MonthNotValid"]
            self.message_MonthEmpty = config["Month"]["message_MonthEmpty"]

    class ShowData:
        def __init__(self):
            self.message_TotalSpent = config["ShowData"]["message_TotalSpent"]
            self.message_YearSpent = config["ShowData"]["message_YearSpent"]
            self.message_MonthSpent = config["ShowData"]["message_MonthSpent"]
            self.message_DateSpent = config["ShowData"]["message_DateSpent"]
            self.message_LeastExpensive = config["ShowData"]["message_LeastExpensive"]
            self.message_MostExpensive = config["ShowData"]["message_MostExpensive"]
    
    class BudgetSystem:
        def __init__(self):
            self.message_FolderTreeDoesntExist = config["BudgetSystem"]["message_FolderTreeDoesntExist"]
        
    class Settings:
        def __init__(self):
            self.message_InvalidConfigFile = config["Settings"]["message_InvalidConfigFile"]
            self.message_UnallocatedConfigFile = config["Settings"]["message_UnallocatedConfigFile"]

def init_language_config() -> None:
    """
       This read the language configuration text file if it was assigned.
    """

    global config
    config = configparser.ConfigParser()
    LANG_ = LANG
    if os.environ.get('CONFIG_BUDGET'):
        config_budget = configparser.ConfigParser()
        config_budget.read(os.environ["CONFIG_BUDGET"], encoding="utf-8")
        LANG_ = config_budget["DEFAULT"]["lang"]
    config.read(os.path.join(current_path, f"languages/{LANG_}.ini"), encoding="utf-8")

def get_month_text() -> Tuple[str]:
    """This gets the text for the Month class"""
    init_language_config()

    lang_month_messages = Language.Month()

    return (
        lang_month_messages.message_MonthNotValid,
        lang_month_messages.message_MonthEmpty
    )

def get_show_data_text() -> Tuple[str]:
    """This gets the text for the show_data"""
    init_language_config()
    
    lang_show_data_messages = Language.ShowData()

    return (
        lang_show_data_messages.message_TotalSpent,
        lang_show_data_messages.message_YearSpent,
        lang_show_data_messages.message_MonthSpent,
        lang_show_data_messages.message_DateSpent,
        lang_show_data_messages.message_LeastExpensive,
        lang_show_data_messages.message_MostExpensive
    )

def get_budget_system_text() -> Tuple[str]:
    """This gets the text for the budget_system"""
    init_language_config()
    
    lang_budget_system_messages = Language.BudgetSystem()

    return (
        lang_budget_system_messages.message_FolderTreeDoesntExist,
    )
    
def get_settings_text() -> Tuple[str]:
    """This gets the text for the settings"""
    init_language_config()

    lang_settings_messages = Language.Settings()

    return (
        lang_settings_messages.message_InvalidConfigFile,
        lang_settings_messages.message_UnallocatedConfigFile,
    )