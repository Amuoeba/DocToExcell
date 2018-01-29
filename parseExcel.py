# -*- coding: utf-8 -*-
import pandas
from pandas import DataFrame
#EXCEL-SPECIFIKACIJE PRODUKTOV.XLSX
#EXCEL STEKELNA EMBALAŽA.XLSX

from termcolor import colored

print (colored('hello', 'red'), colored('world', 'green'))


datasheet = pandas.read_excel("./CsvData/EXCEL-SPECIFIKACIJE PRODUKTOV.XLSX",header=1)


class ExcellWriter():
    def __init__(self,doclist):
        self.doclist = doclist
    