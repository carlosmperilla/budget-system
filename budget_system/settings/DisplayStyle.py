"""This module saves the constants for the data display"""

#ANSI commands to color the shell
from colorama import Style, Fore, Back

#Screen width in characters
WIDTH_CHR = 101

#Color styles for the different sections of the display
STYLE_SEPARATOR = Style.BRIGHT+Fore.BLUE+Back.BLACK
STYLE_DATE =  Style.NORMAL+Fore.RED+Back.WHITE
STYLE_SPENT_MONTH_TITLE = Style.BRIGHT+Fore.WHITE+Back.MAGENTA
STYLE_SPENT_YEAR_TITLE = Style.BRIGHT+Fore.WHITE+Back.CYAN
STYLE_SPENT_TOTAL_TITLE = Style.BRIGHT+Fore.WHITE+Back.RED
STYLE_SPENT_TITLE = Style.DIM+Fore.WHITE+Back.RED
STYLE_SECTOR_TITLE = Style.DIM+Fore.BLACK+Back.GREEN
STYLE_LEAST_EXPENSIVE_TITLE = Style.DIM+Fore.BLACK+Back.YELLOW
STYLE_MOST_EXPENSIVE_TITLE = Style.BRIGHT+Fore.WHITE+Back.YELLOW