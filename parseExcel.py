# -*- coding: utf-8 -*-
import pandas
#EXCEL-SPECIFIKACIJE PRODUKTOV.XLSX
#EXCEL STEKELNA EMBALAŽA.XLSX

from termcolor import colored

print (colored('hello', 'red'), colored('world', 'green'))


datasheet = pandas.read_excel("./CsvData/EXCEL-SPECIFIKACIJE PRODUKTOV.XLSX",header=1)