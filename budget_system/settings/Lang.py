"""This module gets lang"""

#To work with environment variables
import os
#To access the configuration file
import configparser

#To get the system default language
from locale import getdefaultlocale

#Default auxiliary language
AUX_LANG = {
    "es" : "SPA",
    "en" : "ENG",
}.get(getdefaultlocale()[0][:2], "ENG")

#This read the configuration
config = configparser.ConfigParser()
config.read(os.environ.get("CONFIG_BUDGET", ""), encoding="utf-8")

#This gets the language from the config if it exists, otherwise it gets the auxiliary
LANG = config["DEFAULT"].get("lang", AUX_LANG)
