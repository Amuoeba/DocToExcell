# -*- coding: utf-8 -*-
import os
from bs4 import BeautifulSoup
import re
from pandas import DataFrame
import pandas as pd
import numpy as np
from collections import OrderedDict
from FormattingTools import extractBasic
from FormattingTools.helper_classes import Attribute as A
from FormattingTools import markers


class DocumentHTML():
    
    DocType = "1: Normal Tabled"
    
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
        self.Naziv = self.FindNaziv()
        self.Opis = extractBasic.opisIzdelka(self.FormatedRows)
        self.Sestavine = extractBasic.sestavine(self.FormatedRows)
        self.Senzorika = extractBasic.senzorika(self.FormatedRows)
        self.Mikrobioloske = extractBasic.microbiological(self.FormatedRows)
        self.FizKem = extractBasic.fizikalnoKemijske(self.FormatedRows)
        self.HranilnaVrednost = extractBasic.hranilnaVrednost(self.FormatedRows)
        self.AktivneUcinkovine = extractBasic.aktivneUcinkovine(self.FormatedRows)
        self.Pakiranje = extractBasic.pakiranje(self.FormatedRows)
        self.Zakonodaja = extractBasic.zakonodaja(self.FormatedRows)
        #Data Frames
        self.dataFrames = self.PrepareDataFrames()
        # All attributes
        self.allAtributes = self.getAtributes()
        
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
#        if self.doc_name == "./RealDataHTML2/SP 32313020 APISIRUP (JUNIOR) 140 ML AR-AN.html":
#            for i in txtRows:
#                print(i)        
        toInsert = None
        for row in txtRows:
            for secMarker in markers.SECTION_MARKERS:
                m = markers.SECTION_MARKERS[secMarker]
                if bool(re.search(m,row[0])):
                    toInsert = secMarker
            if toInsert and not bool(re.search(markers.SECTION_MARKERS[toInsert],row[0])):
                row.insert(0,toInsert)               
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
                    return A("Datum Izdaje",value=item)
        return None
    
    def FindCode(self):
        reCode = re.compile("(?:Šifra:)(?: *)([0-9]*)",re.IGNORECASE)
        match = re.search(reCode,self.FormatedRows[0][1])
        if bool(match):
            return A("Šifra",match.group(1))
        else:
            return None
    def FindNaziv(self):
        reCode = re.compile("(?<=PROIZVODA )(.*)(?= Šifra)",re.IGNORECASE)
        match = re.search(reCode,self.FormatedRows[0][1])
        if bool(match):
            return A("Naziv",match.group(0))
        else:
            return None
        
        
    # Getting a list of all atributes
    def getAtributes(self):
        attrSet = set([])
        if self.Opis:
            attrSet.add(self.Opis.name)
        if self.Sestavine:
            attrSet.add(self.Sestavine.name)
        if self.Senzorika:
            for a in self.Senzorika:
                assert isinstance(a,A)
                if a.name not in attrSet:
                    attrSet.add(a.name)
        if self.Mikrobioloske:
            for a in self.Mikrobioloske:
                assert isinstance(a,A)
                if a.name not in attrSet:
                    attrSet.add(a.name)
        if self.FizKem:
            for a in self.FizKem:
                assert isinstance(a,A)
                if a.name not in attrSet:
                    attrSet.add(a.name)
        if self.AktivneUcinkovine:                    
            for a in self.AktivneUcinkovine:
                assert isinstance(a,A)
                if a.name not in attrSet:
                    attrSet.add(a.name)
        if self.HranilnaVrednost:
            for a in self.HranilnaVrednost:
                assert isinstance(a,A)
                if a.name not in attrSet:
                    attrSet.add(a.name)
        if self.Pakiranje:                    
            for a in self.Pakiranje:
                assert isinstance(a,A)
                if a.name not in attrSet:
                    attrSet.add(a.name)
        return attrSet
        
    # Getting sections
    #Preparing dataframes
    def PrepareDataFrames(self):
        dataframes = {}
        dataframes["Šifra"] = self.prepSifra()
        dataframes["Naziv"] = self.prepNaziv()
#        dataframes["Skupina"] = DataFrame({"Skupina":["/"]})
        dataframes["Opis"] = self.prepOpis()
#        dataframes["Sestavine"] = DataFrame({"Sestavine":[self.Sestavine]})
#        dataframes["Izgled"] = DataFrame({"Izgled":[self.Izgled]})
#        dataframes["Okus In Vonj"] = DataFrame({"Okus in Vonj":[self.Vonj]})
#        dataframes["Zakonodaja"] = DataFrame({"Zakonodaja":[self.Zakonodaja]})
#        dataframes["Mikrobiološke Zahteve"] = self.HEADER_DFMikrobioloske()
#        dataframes["Fizikalno Kemijske Zahteve"] = self.HEADER_DFfizikalno_kemijske()
#        dataframes["Hranilna Vrednost"] = self.HEADER_DFhranilna_vrednost()
#        dataframes["Aktivne učinkovine"] = self.HEADER_DFaktivne_ucinkovine()
#        dataframes["Pakiranje"] = self.DFpakiranje()        
        return dataframes
    
    def prepSifra(self):
        if self.Sifra:
            columns = [self.Sifra.name]
            values = [self.Sifra.value]
            return DataFrame([values],columns=columns)
        else:
            return DataFrame([np.NaN])
    
    def prepNaziv(self):
        if self.Naziv:
            columns = [self.Naziv.name]
            values = [self.Naziv.value]
            return DataFrame([values],columns=columns)
        else:
            return DataFrame([np.NaN])
        
    def prepOpis(self):
        if self.Opis:
            columns = [self.Opis.name]
            values = [self.Opis.value]
            return DataFrame([values],columns=columns)
        else:
            return DataFrame([np.NaN])
    
    
    # Printing functions
    def printSifra(self):
        self.Sifra.nicePrint()
        
    def printDatumIzdaje(self):
        self.DatumIzdaje.nicePrint()
    
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


    def Print_FizKem(self):
        print(self.doc_name)
        if self.FizKem:
            for i in self.FizKem:
                assert isinstance(i,A)
                print("Name: ",i.name,"Value:",i.value,"Max:",i.Max,"Min:",i.Min,"Unit:",i.unit,"PDV",i.pdv)
    
    def Print_Mikrobioloske(self):
        print(self.doc_name)
        if self.Mikrobioloske:
            for i in self.Mikrobioloske:
                assert isinstance(i,A)
                print("Name: ",i.name,"Value:",i.value,"Max:",i.Max,"Min:",i.Min,"Unit:",i.unit,"PDV",i.pdv)
    
    def Print_HranilnaVrednost(self):
        print(self.doc_name)
        if self.HranilnaVrednost:
            for i in self.HranilnaVrednost:
                assert isinstance(i,A)
                print("Name: ",i.name,"Value:",i.value,"Max:",i.Max,"Min:",i.Min,"Unit:",i.unit,"Per:",i.per,"PDV",i.pdv,"CommonName:",i.commonName)
                
    def Print_AktivneUcinkovine(self):
#        print(self.doc_name)
#        if self.AktivneUcinkovine:
##            print(self.AktivneUcinkovine[0])
#            for i in self.AktivneUcinkovine:
#                print(i[1])
        print(self.doc_name)
        if self.AktivneUcinkovine:
            for i in self.AktivneUcinkovine:
                assert isinstance(i,A)
                print("Name: ",i.name,"Value:",i.value,"Max:",i.Max,"Min:",i.Min,"Unit:",i.unit,"Per:",i.per,"PDV",i.pdv)
    
    def Print_Pakiranje(self):
        print(self.doc_name)
        if self.Pakiranje:
            for i in self.Pakiranje:
                assert isinstance(i,A)
                print("Name: ",i.name,"Value:",i.value)

    def Print_Zakonodaja(self):
        print(self.doc_name)
        if self.Zakonodaja:
            for i in self.Zakonodaja:
                assert isinstance(i,A)
                print("Name: ",i.name,"Value:",i.value)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    