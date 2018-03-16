# -*- coding: utf-8 -*-
from termcolor import colored
import re
from FormattingTools import markers

class Attribute():    
    def __init__(self,name,value = None,Min = None,Max = None,unit = None):
        self.name = name
        self.value = value
        self.Max = Max
        self.Min = Min
        self.unit = unit
    
    def nicePrint(self):
        print("Name: ",self.name,"Value: ",self.value,"Max: ",self.Max,"Min: ",self.Min,"unit: ",self.unit )
    

class RowFormat():
    def __init__(self,row):
        self.regex = {"unit":markers.UNITS,"number":re.compile("[0-9]+(?:[,.]*[0-9]*)",re.IGNORECASE),"max":markers.MAX, "min":markers.MIN}
        self.raw_row = row
        self.no_entries = len(self.raw_row)
        self.catRow = self.categorizeElements()
        
    def categorizeElements(self):
        row = self.raw_row        
        row_cat = []
        for element in row:
            eleCat = {}
            for reg in self.regex:
                checker = getMatch(re.findall(self.regex[reg],element),variant=reg)
                if checker:
                    eleCat[reg] = checker
                else:
                    eleCat[reg] = None
            row_cat.append(eleCat)
        
        return row_cat




def getMatch(matches,variant = "min"):    
    if len(matches) > 0 and not(len(matches) == 2 and (variant == "min" or variant == "max")):
        if isinstance(matches[0],tuple):
            value = [x for x  in matches[0] if x != ""]
        else:
            value = matches
    elif len(matches) == 2 and (variant == "min" or variant == "max"):
        extMatches = []
        for x in matches:
            if isinstance(x,tuple):
                for i in x:
                    if i != "":
                        extMatches.append(i)
            else:
                extMatches.append(x)
        if variant == "min":
            value = [extMatches[0]]
        else:
            value = [extMatches[-1]]
        
    else:
        value = None
    return value 