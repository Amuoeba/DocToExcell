# -*- coding: utf-8 -*-
from termcolor import colored
import re
from FormattingTools import markers

class Attribute():    
    def __init__(self,name,value = None,Min = None,Max = None,unit = None,per = None):
        self.name = name
        self.value = value
        self.Max = Max
        self.Min = Min
        self.unit = unit
        self.per = per
    
    def nicePrint(self):
        print("Name: ",self.name,"Value: ",self.value,"Max: ",self.Max,"Min: ",self.Min,"unit: ",self.unit,"Per: ",self.per )
    

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
    
    def matchAtDifferent(tupList):
        index = []
        for ele in tupList:
            for j in enumerate(ele):
                if j[1] == '':
                    index.append(j[0])
        if len(set(index)) == 1:
            return False
        else:
            return True
        
    
    if len(matches) > 0 and not(len(matches) == 2 and (variant == "min" or variant == "max") and matchAtDifferent(matches)):
        if isinstance(matches[0],tuple):
            value = [[y for y in x if y != ''][0] for x in matches]
        else:
            value = matches
    elif len(matches) == 2 and (variant == "min" or variant == "max") and matchAtDifferent(matches):
        extMatches = []
        print(matches)
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