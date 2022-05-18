"""This module generates types for Spent"""

#To generate types
from typing import NewType
from typing import Tuple, Dict

#Types for DataFrames
from numpy import float64
from pandas.core.frame import DataFrame

#Types for Spent 
ProductsData = NewType('ProductsData', Tuple[DataFrame, DataFrame, float64])
DatesDict = NewType('DatesDict', Dict[str, ProductsData])
SectorsDict = NewType('SectorsDict', Dict[str, DatesDict])
MonthData = NewType('MonthData', Tuple[SectorsDict, float64])
YearData = NewType('YearData',  Tuple[Dict[str, MonthData], float64])
TotalData = NewType('TotalData',  Tuple[Dict[int, YearData], float64])