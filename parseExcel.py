# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame
from fuzzywuzzy import fuzz
#EXCEL-SPECIFIKACIJE PRODUKTOV.XLSX
#EXCEL STEKELNA EMBALAŽA.XLSX

from termcolor import colored

print (colored('hello', 'red'), colored('world', 'green'))


datasheet = pd.read_excel("./CsvData/SPECIFIKACIJE-POPIS PARAMETROV - Rok.xlsx",header=1)


class ExcellWriter():
    def __init__(self,doclist):
        self.doclist = doclist
    



l1 = [1,2,3,4]
l2 = [1,2,3,4]
df = DataFrame({'Stimulus Time': l1, 'Reaction Time': l2})
df.to_excel('test.xlsx', sheet_name='sheet1', index=False)

df = pd.read_excel("test.xlsx")
writer = pd.ExcelWriter("test.xlsx",engine="openpyxl")
df.to_excel(writer, index=False)
df.to_excel(writer, startrow=len(df)+1, index=False,header=None)
writer.save()

def findHighestMatch(string,lst):
    def findHighestMatchAUX(s,l):
        h = 0
        for i in l:
            dist = fuzz.partial_ratio(s.lower(),i.lower())
            if dist >= h:
                h = dist
        return h
    highest = None
    highestDist = 0
    
    for i in lst:
        i = i.split()
        s = string.split()
        matchesList = []
        for ele in i:
            hm = findHighestMatchAUX(ele,s)
            matchesList.append(hm)
        
        avgMatch = sum(matchesList)/len(matchesList)
        if avgMatch >= highestDist:
            highestDist = avgMatch
            highest = (string,i)
    
    return highest