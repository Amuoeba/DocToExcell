# -*- coding: utf-8 -*-
from pandas import DataFrame
import parseXML
import pandas as pd
import numpy as np

class writeExcell():
    def __init__(self,dataframe):
        self.dataframe = dataframe
        self.index = pd.Index(["Šifra","Naziv","Skupina","Opis","Sestavine","Izgled","Okus In Vonj","Zakonodaja"])
        
        
    
    def createDocDataframe(self,document):
        assert isinstance(document,parseXML.Document)

        docDF = DataFrame({"Šifra":[self.NA(document.Sifra)]})
        docDF["Naziv"] = [self.NA(document.Naziv)]
        docDF["Skupina"] = ["/"]
        docDF["Opis"] = [self.NA(document.OpisIzdelka)]
        docDF["Sestavine"] = [self.NA(document.Sestavine)]
        docDF["Izgled"] = [self.NA(document.Izgled)]
        docDF["Okus In Vonj"] = [self.NA(document.Vonj)]
        docDF = self.setMIKROBIOLOSKE(docDF,document)
        docDF = self.setFIZIKALNO_KEMIJSKE_ZAHTEVE(docDF,document)
        docDF["Zakonodaja"] = [self.NA(document.Zakonodaja)]
        
        
        
        print(docDF.columns)
        if self.dataframe is not None:
            self.dataframe = pd.concat([self.dataframe,docDF],axis=0,ignore_index=True)
            self.dataframe = self.dataframe.reindex_axis(self.index,axis=1)
        else:
            self.dataframe = docDF
    
    def setMIKROBIOLOSKE(self,documentDF,document):
        assert isinstance(document,parseXML.Document)
        if document.MikrobiloskeZahteve:
            for entry in document.MikrobiloskeZahteve:
                if entry not in self.index:
                    self.index = self.index.append(pd.Index([entry]))
                documentDF[entry] = [document.MikrobiloskeZahteve[entry]]        
            return documentDF
        else:
            return documentDF
    
    def setFIZIKALNO_KEMIJSKE_ZAHTEVE(self,documentDF,document):
        assert isinstance(document,parseXML.Document)
        if document.FizikalnoKemijskeZahteve:
            for entry in document.FizikalnoKemijskeZahteve:
                if entry not in self.index:
                    self.index = self.index.append(pd.Index([entry]))
                documentDF[entry] = [document.FizikalnoKemijskeZahteve[entry]]
            return documentDF
        else:
            return documentDF
    
    def write(self,path):
        writer = pd.ExcelWriter(path,engine="openpyxl")
        self.dataframe.to_excel(writer, index=False)
        writer.save()
        
    def NA(self,val):
        if val:
            return val
        else:
            return "NA"