"""This module gets config for budget"""

#To work with environment variables and paths
import os
#To access the configuration file
import configparser

from .LanguagesText import get_settings_text

class ConfigBudget:
    """Application global configuration, requires a config.ini file
    to have been created and define an environment variable CONFIG_BUDGET 
    with its path.
    """
    class UnallocatedConfigFile(KeyError):
        """Config file not located error."""
        pass

    class InvalidConfigFile(Exception):
        """Config file not valid error."""
        pass

    config = configparser.ConfigParser()

    CONFIG_FILE_NAME = 'config.ini'

    message_InvalidConfigFile,\
    message_UnallocatedConfigFile = get_settings_text()

    def __init__(self) -> None:
        self.try_to_read()

    def check_configfile_name(self, config_file_path:str) -> None:
        """This checks if the configuration path is valid.
        """
        return os.path.split(config_file_path)[1] == self.CONFIG_FILE_NAME 

    def valid_configfile(self, config_file_path:str) -> None:
        """This checks if the configuration path is valid.
        On error: raise InvalidConfigFile
        """
        if not self.check_configfile_name(config_file_path):
            raise ConfigBudget.InvalidConfigFile(self.message_InvalidConfigFile)

    def read_config(self) -> None:
        """This gets the config file path from the CONFIG_BUDGET environment variable,
        validates it, and reads it.
        """
        self.CONFIG_FILE_PATH = os.environ["CONFIG_BUDGET"]
        self.valid_configfile(self.CONFIG_FILE_PATH)
        self.config.read(self.CONFIG_FILE_PATH, encoding="utf-8")

    def assign_constants(self) -> None:
        """This assigns configuration constants, mainly for Spent and PurchaseList."""
        self.PRICE_NAME = self.config["DEFAULT"]["price_name"]
        self.BASE_PATH = self.config["DEFAULT"]["base_path"]
        self.YEAR_PATH = os.path.join(self.BASE_PATH, "{year}")
        self.MONTH_PATH = os.path.join(self.YEAR_PATH, "{month}")
        self.TABLE_PATH = os.path.join("{month_path}", "{table_name}")

    def try_to_read(self) -> None:
        """This tries to read the configuration file. It then assigns the configuration constants.
        On error: raise UnallocatedConfigFile           
        """
        try:
            self.read_config()
            self.assign_constants()
        except KeyError:
            raise ConfigBudget.UnallocatedConfigFile(self.message_UnallocatedConfigFile) from KeyError

    def get_paths(self) -> None:
        """This gets all constant paths."""
        return (
            self.BASE_PATH,
            self.YEAR_PATH, 
            self.MONTH_PATH, 
            self.TABLE_PATH,
            )
