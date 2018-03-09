# -*- coding: utf-8 -*-

import os
from bs4 import BeautifulSoup
import re
from pandas import DataFrame
import pandas as pd
import numpy as np
from collections import OrderedDict
from FormattingTools import extractBasic
from FormattingTools.attribute import Attribute as A


class DocumentHTML():  
    
    
    def __init__(self,doc_path):
        self.doc_name = doc_path
        self.document = open(doc_path,"rb")
        self.doc_soup = BeautifulSoup(self.document,'html.parser')
        self.RAW_rows = None
        self.rows = self.findRows()
        self.FormatedRows = self.formatRows()
        
        # Atributes
        self.DatumIzdaje = self.FindDatumIzdaje()
        self.Sifra = self.FindCode()
        self.Opis = extractBasic.opisIzdelka(self.FormatedRows)
        self.Sestavine = extractBasic.sestavine(self.FormatedRows)
        self.Senzorika = extractBasic.senzorika(self.FormatedRows)
        
    # Getting structured information for each row
    def findRows(self):
#        AUXtxtEntries = self.doc_soup.find_all("p")
#        txtEntries = []
#        for ele in AUXtxtEntries:
#            if ele.find_all("table",recusive=False) == []:
#                txtEntries.append(ele)
#        rows = []
#        checkRow = set([])
#        for ele in txtEntries:
#            row = self.botomUp(ele)
#            if row:
#                if row not in checkRow:
#                    rows.append(row)
#                    checkRow.add(row)
        
        tables = self.doc_soup.find_all("table")
        rows = []
        for tab in tables:            
            auxRows = tab.find_all("tr")
            for row in  auxRows:
                if row.find_all("table") == []:
                    rows.append(row)
        
        self.RAW_rows = rows
        
        text_by_row = []
        aux = set()        
        for row in rows:
            tx = self.findAllTextEntries(row)
            aux_tx = str(tx)
##            print(aux_tx)
            if aux_tx not in aux or tx[0][0] == '':
                text_by_row.append(tx)
                aux.add(aux_tx)            
        return text_by_row
    
    def findAllTextEntries(self,soup):
        """Extract just text entries sequentially"""
        txtEntries = soup.find_all("td")#(attrs={"lang":"sl-SI"})
        spans = []
        for i in enumerate(txtEntries):
            if i[1].has_key("rowspan"):
                rowSpan = int(i[1]["rowspan"])
                colPos = i[0]
                spans.append((colPos,rowSpan))
            else:
                rowSpan = 1
                colPos = i[0]
                spans.append((colPos,rowSpan))                
        txtEntries = [x  for x in txtEntries if x.text != "\n"]
        txtEntries = [re.sub("[\t\n]"," ",x.text) for x in txtEntries]
        txtEntries = [re.sub(" +"," ",x) for x in txtEntries]
        txtEntries = [x.rstrip() for x in txtEntries]
        txtEntries = [x.lstrip() for x in txtEntries]
        
        metaTextEnt = []
        for x in enumerate(txtEntries):
            metaTextEnt.append((x[1],spans[x[0]][0],spans[x[0]][1]))
        
        return metaTextEnt
    
    def formatRows(self):
        txtRows = []
        for row in self.rows:
            elements = [x[0] for x in row]
            txtRows.append(elements)
        
        for row in enumerate(self.rows):
            rowIndex = row[0]
            for ele in row[1]:
                if ele[2] > 1:
                    for r in list(range(rowIndex,rowIndex+ele[2]))[1:]:
                        txtRows[r].insert(ele[1],ele[0])
        #self.removeBlanks(list(OrderedDict.fromkeys(x)))
        txtRows = [self.removeBlanks(x) for x in txtRows if not all(i == '' for  i in x)]
        
        return txtRows
    
    def removeBlanks(self,row):
        return [x for x in row if x != '']
    
    def botomUp(self,textele):
        if textele:
            if textele.name == "tr":
                return textele
            else:
                return self.botomUp(textele.parent)
        else:
            return None
    # Extracting document info
    def FindDatumIzdaje(self):
        reDatum = re.compile("datum izdaje",re.IGNORECASE)
        for row in self.FormatedRows:
            for item in row:
                if bool(reDatum.match(item)):
                    return item
        return None
    
    def FindCode(self):
        reCode = re.compile("(?:Šifra:)(?: *)([0-9]*)",re.IGNORECASE)
        match = re.search(reCode,self.FormatedRows[0][1])
        if bool(match):
            return match.group(1)
        else:
            return "Ni šifre"
    # Getting sections
    
    # Printing functions
    def printOpis(self):
        assert isinstance(self.Opis,A)
        print(self.Opis.name,self.Opis.value)
    
    def printSestavine(self):
        assert isinstance(self.Sestavine,A)
        print(self.Sestavine.name,self.Sestavine.value)
    
    def printSenzorika(self):
#        assert isinstance(self.Sestavine,A)
        for i in self.Senzorika:
            assert isinstance(i,A)
            print(i.name,i.value)
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    