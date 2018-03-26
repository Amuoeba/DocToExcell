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
from FormattingTools import aux_tools
from FormattingTools.aux_tools import listToString as lts


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
        dataframes["Sestavine"] = self.prepSestavine()
        dataframes["Senzorika"] = self.prepSenzorika()
#        dataframes["Izgled"] = DataFrame({"Izgled":[self.Izgled]})
#        dataframes["Okus In Vonj"] = DataFrame({"Okus in Vonj":[self.Vonj]})
        dataframes["Zakonodaja"] = self.prepZakonodaja()
        dataframes["Mikrobiološke Zahteve"] = self.prepMikrobioloske()
        dataframes["Fizikalno Kemijske Zahteve"] = self.prepFizikalne()
        dataframes["Hranilna Vrednost"] = self.prepHranilnaVrednost()
        dataframes["Aktivne učinkovine"] = self.prepAktivne()
        dataframes["Pakiranje"] = self.prepPakiranje()     
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
        
    def prepSestavine(self):
        if self.Opis:
            columns = [self.Sestavine.name]
            values = [self.Sestavine.value]
            return DataFrame([values],columns=columns)
        else:
            return DataFrame([np.NaN])
    
    def prepSenzorika(self):
        if self.Senzorika:
            columns = []
            values = []
            for item in self.Senzorika:
                assert isinstance(item,A)
                columns.append(item.commonName)
                values.append(item.value)      
            return DataFrame([values],columns=columns)
        else:
            return DataFrame([np.NaN])
    
    def prepZakonodaja(self):
        if self.Zakonodaja:
            columns = []
            values = []
            for item in self.Zakonodaja:
                assert isinstance(item,A)
                columns.append(item.name + " value")
                values.append(item.value)                    
                
            return DataFrame([values],columns=columns)
        else:
            return DataFrame([np.NaN])
    
    def prepMikrobioloske(self):
        if self.Mikrobioloske:
            columns = []
            values = []            
            for item in self.Mikrobioloske:
                assert isinstance(item,A)
                columns.append(item.commonName + " [value]")
                values.append(item.value)                
                columns.append(item.commonName + " [max]")
                values.append(item.Max)                
                columns.append(item.commonName + " [min]")
                values.append(item.Min)                
                columns.append(item.commonName + " [unit]")
                values.append(item.unit)            
            return DataFrame([values],columns=columns)            
        else:
            return DataFrame([np.NaN])
    
    def prepHranilnaVrednost(self):       
        if self.HranilnaVrednost:
            columns = []
            values = []
            
            allreadyIn = set([])
            for item in self.HranilnaVrednost:
                assert isinstance(item,A)
                name = item.commonName
                value = item.value
                Max = item.Max
                Min = item.Min
                pdv = item.pdv
                per = item.per
                unit = item.unit
                
                longest = aux_tools.findLongest([value,Max,Min,unit])
                if unit:
                    lenUnit = len(unit)
                else:
                    lenUnit = 0
                
                if lenUnit > 1 or lenUnit != len(longest) and name not in allreadyIn:
                    for ind in range(lenUnit):
                        n = name + " " + str(ind)
                        if len(value) >= ind and n not in allreadyIn:
                            v = [value[ind]]
                            u = [unit[ind]]
                            columns.append("[HV] " + n + " [value]")
                            values.append(v)
                            columns.append("[HV] " + n + " [per]")
                            values.append(per)
#                            columns.append("[HV] " + n + " [max]")
#                            values.append(Max)
#                            columns.append("[HV] " + n + " [min]")
#                            values.append(Min)
                            columns.append("[HV] " + n + " [unit]")
                            values.append(u)
                            columns.append("[HV] " + n + " [pdv]")
                            values.append(pdv)
                            allreadyIn.add(n)
                else:
                    if name not in allreadyIn:
                        columns.append("[HV] " + name + " [value]")
                        values.append(value)
                        columns.append("[HV] " + name + " [per]")
                        values.append(per)
                        columns.append("[HV] " + name + " [max]")
                        values.append(Max)
                        columns.append("[HV] " + name + " [min]")
                        values.append(Min)
                        columns.append("[HV] " + name + " [unit]")
                        values.append(unit)
                        columns.append("[HV] " + name + " [pdv]")
                        values.append(pdv)                    
                        allreadyIn.add(name)
                    
            return DataFrame([values],columns=columns)  
        else:
            return DataFrame([np.NaN])
    
    def prepFizikalne(self):
        if self.FizKem:
            columns = []
            values = []
            
            allreadyIn = set([])
            for item in self.FizKem:
                assert isinstance(item,A)
                name = item.commonName
                value = item.value
                Max = item.Max
                Min = item.Min
                pdv = item.pdv
                per = item.per
                unit = item.unit
                
                if name not in allreadyIn:
                    columns.append("[FK] " + name + " [value]")
                    values.append(value)
                    columns.append("[FK] " + name + " [max]")
                    values.append(Max)
                    columns.append("[FK] " + name + " [min]")
                    values.append(Min)
                    columns.append("[FK] " + name + " [unit]")
                    values.append(unit)
                    columns.append("[FK] " + name + " [pdv]")
                    values.append(pdv)
                    
                    allreadyIn.add(name)
                    
            return DataFrame([values],columns=columns)  
        else:
            return DataFrame([np.NaN])

    def prepAktivne(self):
        if self.AktivneUcinkovine:
            columns = []
            values = []
            
            allreadyIn = set([])
            for item in self.AktivneUcinkovine:
                assert isinstance(item,A)
                name = item.commonName
                value = item.value
                Max = item.Max
                Min = item.Min
                pdv = item.pdv
                per = item.per
                unit = item.unit
                
                longest = aux_tools.findLongest([value,Max,Min,unit])
                if unit:
                    lenUnit = len(unit)
                else:
                    lenUnit = 0
                
                if lenUnit > 1 or lenUnit != len(longest) and name not in allreadyIn:
                    for ind in range(lenUnit):
                        n = name + " " + str(ind)
                        if len(value) >= ind and n not in allreadyIn:
                            v = [value[ind]]
                            u = [unit[ind]]
                            columns.append("[A] " + n + " [value]")
                            values.append(v)
                            columns.append("[A] " + n + " [per]")
                            values.append(per)
#                            columns.append("[HV] " + n + " [max]")
#                            values.append(Max)
#                            columns.append("[HV] " + n + " [min]")
#                            values.append(Min)
                            columns.append("[A] " + n + " [unit]")
                            values.append(u)
                            columns.append("[A] " + n + " [pdv]")
                            values.append(pdv)
                            allreadyIn.add(n)
                
                else:
                    if name not in allreadyIn:
                        columns.append("[A] " + name + " [value]")
                        values.append(value)
                        columns.append("[A] " + name + " [max]")
                        values.append(Max)
                        columns.append("[A] " + name + " [min]")
                        values.append(Min)
                        columns.append("[A] " + name + " [unit]")
                        values.append(unit)
                        columns.append("[A] " + name + " [pdv]")
                        values.append(pdv)                    
                        allreadyIn.add(name)
                    
            return DataFrame([values],columns=columns)  
        else:
            return DataFrame([np.NaN])
    def prepPakiranje(self):
        if self.Pakiranje:
            columns = []
            values = []
            
            allreadyIn = set([])
            for item in self.Pakiranje:
                assert isinstance(item,A)
                name = item.commonName
                value = item.value
                Max = item.Max
                Min = item.Min
                pdv = item.pdv
                per = item.per
                unit = item.unit
                
                if name not in allreadyIn:
                    columns.append("[PAK] " + name + " [value]")
                    values.append(value)
                    columns.append("[PAK] " + name + " [max]")
                    values.append(Max)
                    columns.append("[PAK] " + name + " [min]")
                    values.append(Min)
                    columns.append("[PAK] " + name + " [unit]")
                    values.append(unit)
                    columns.append("[PAK] " + name + " [pdv]")
                    values.append(pdv)
                    
                    allreadyIn.add(name)
                    
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
            print(i.commonName)  


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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    