# -*- coding: utf-8 -*-
from termcolor import colored
import re
from FormattingTools import markers
from FormattingTools import aux_tools

class Attribute():    
    def __init__(self,name,value = None,Min = None,Max = None,unit = None,per = None):
        self.name = name
        self.value = value
        self.Max = Max
        self.Min = Min
        self.unit = unit
        self.per = per
        self.pdv = self.getPDV()
        self.commonName = self.setCommonClass()
    
    def getPDV(self):
        if self.unit:
            pdvInd = None
            for u in enumerate(self.unit):
                if u[1] == "%" and self.value and self.unit and len(self.unit)==len(self.value):
                    pdvInd = u[0]            
            pdv = None
#            print(self.value,self.unit,self.Max,self.Min)
            if pdvInd:
                pdv = self.value[pdvInd]      
                del self.value[pdvInd]
                del self.unit[pdvInd]
            
            return pdv
    
    def setCommonClass(self):
        joiners = markers.JOIN_MARKERS
        for marker in joiners:
            match = re.findall(joiners[marker],self.name)
            if match != []:
                return marker        
        return self.name
            
               
        
        
    def nicePrint(self):
        print("Common name:",self.commonName,"Name: ",self.name,"Value: ",self.value,"Max: ",self.Max,"Min: ",self.Min,"unit: ",self.unit,"Per: ",self.per,"PDV: ",
              self.pdv )
    
    

class RowFormat():
    def __init__(self,row):
        self.regex = {"unit":markers.UNITS,"number":re.compile("[0-9]+(?:[,.]*[0-9]*)",re.IGNORECASE),"max":markers.MAX, "min":markers.MIN}
        self.raw_row = row
        self.no_entries = len(self.raw_row)        
        self.catRow = self.categorizeElements()
        self.header = self.isHeader()
        
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
    
    def isHeader(self):
        for entry in self.raw_row:
            reg = markers.AKTIVNE["Na"]
            matches = re.findall(reg,entry)
            if matches != []:
                return True
        return False
    
    
    
    def splitRow(self,split):
        newCatRow = []
        for entry in self.catRow[:2]:
            newCatRow.append(entry)
        for entry in self.catRow[2:]:
            present = list(entry.values())            
            if any(present):
                chunkedEntry = {}
                for a in entry:
                    if entry[a]:
                        chunkedEle = aux_tools.chunkList(entry[a],len(entry[a])/(split+1))
                    else:
                        chunkedEle = entry[a]
                    chunkedEntry[a] = chunkedEle
                for i in range(split+1):
                    newEntry = {}
                    for e in chunkedEntry:
                        if chunkedEntry[e]:
                            newEntry[e] = chunkedEntry[e][i]
                        else:
                            newEntry[e] = chunkedEntry[e]
                    newCatRow.append(newEntry)
            else:
                newCatRow.append(entry)
        self.catRow = newCatRow

                            



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
#        print(matches)
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