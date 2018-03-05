# -*- coding: utf-8 -*-

import os
from bs4 import BeautifulSoup
import re
from pandas import DataFrame
import pandas as pd
import numpy as np


class DocumentHTML():
    
    DocType = "1: Normal Tabled"
    
    def __init__(self,doc_path):
        self.doc_name = doc_path
        self.document = open(doc_path,"rb")
        self.doc_soup = BeautifulSoup(self.document,'html.parser')
        self.RAW_rows = None
        self.rows = self.findRows()
        self.FormatedRows = self.formatRows()
        self.DatumIzdaje = self.FindDatumIzdaje()
        self.Sifra = self.FindCode()
        
        
    # Getting structured information for each row
    def findRows(self):
        AUXtxtEntries = self.doc_soup.find_all("p")
        txtEntries = []
        for ele in AUXtxtEntries:
            if ele.find_all("table",recusive=False) == []:
                txtEntries.append(ele)
        rows = []
        for ele in txtEntries:
            row = self.botomUp(ele)
            if row:
                rows.append(row)
        
        self.RAW_rows = rows
        text_by_row = []
        aux = set()   
        
        for row in rows:
            tx = self.findAllTextEntries(row)
            aux_tx = str(tx)
#            print(aux_tx)
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
        txtRows = [x for x in txtRows if not all(i == '' for  i in x)]
        
        return txtRows
    
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
    #Getting sections