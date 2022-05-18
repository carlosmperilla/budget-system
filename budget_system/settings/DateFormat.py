"""This module gets date format"""

#To work with environment variables
import os
#To access the configuration file
import configparser

#Default auxiliary date
AUX_DATE_FORMAT = "%d-%m-%y"

#This read the configuration
config = configparser.ConfigParser()
config.read(os.environ.get("CONFIG_BUDGET", ""), encoding="utf-8")

#This gets the date format from the config if it exists, otherwise it gets the auxiliary
DATE_FORMAT = config["DEFAULT"].get("date_format", AUX_DATE_FORMAT)
