# -*- coding: utf-8 -*-
from pandas import DataFrame
import parseXML
import prepareUnstrructured as pU
import pandas as pd
import numpy as np

class ExcellWriter():
    def __init__(self,doclist):
        self.documents = doclist
        self.UnstructDF = {}
        self.conSec = self.concatSections()
        self.index = self.buildIndex()
        self.DF = self.joinSections()       
        
    
    def concatSections(self):
        DFs = {}
        for document in self.documents:
            if document.DocType == "1: Normal Tabled":
                assert isinstance(document,parseXML.Document)
                #Change this to prepare different output
                for section in document.HEADER_Dataframes:
                    df = document.HEADER_Dataframes
                    if section not in DFs:                 
                        DFs[section] = [df[section]]
                    else:
                        DFs[section].append(df[section])
                        
            elif document.DocType == "2: Only textual":
                assert isinstance(document, pU.DocumentUnstructured)
                for attr in document.Attributes:
                    at = attr[0]
                    val = attr[1]
                    if at not in self.UnstructDF:
                        self.UnstructDF[at] = [val]
                    else:
                        self.UnstructDF[at] = self.UnstructDF[at] +[val] 
        for section in DFs:
            DFs[section] = pd.concat(DFs[section],axis=0,ignore_index=True)        
        return DFs
    
    def joinSections(self):
        secDfList = [self.conSec[x] for x in self.conSec]
        df = pd.concat(secDfList,axis=1,ignore_index=False)
        df.reindex_axis(self.index,axis=1)
        cols = [x for x in df.columns if x != 0]
        return df[cols]
    
    def buildIndex(self):
        sectionOrder = ["Šifra","Naziv","Skupina","Opis","Sestavine","Izgled",
                 "Okus In Vonj","Zakonodaja","Mikrobiološke Zahteve",
                 "Fizikalno Kemijske Zahteve","Hranilna Vrednost","Aktivne učinkovine","Pakiranje"]
        indList = []
        for s in sectionOrder:
            indList = indList + list(self.conSec[s].columns.values)        
        return pd.Index(indList)
    
    def write(self,path,path2):
        writer = pd.ExcelWriter(path,engine="xlsxwriter")
        writerUnstructured = pd.ExcelWriter(path2,engine="openpyxl")
        Ud = pd.DataFrame(self.UnstructDF)
        self.DF.to_excel(writer, index=False,sheet_name='Sheet1')
        Ud.to_excel(writerUnstructured,index=False)
        
        ########## Just formating##############################
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']        
        wrap_format = workbook.add_format({'text_wrap': True})
        worksheet.set_column("A:BL", None, wrap_format)
        #######################################################
        
        writer.save()
        writerUnstructured.save()
    
        
#class writeExcell():
#    def __init__(self,dataframe):
#        self.dataframe = dataframe
#        self.index = pd.Index(["Šifra","Naziv","Skupina","Opis","Sestavine","Izgled","Okus In Vonj","Zakonodaja"])
#        
#        
#    
#    def createDocDataframe(self,document):
#        assert isinstance(document,parseXML.Document)
#
#        docDF = DataFrame({"Šifra":[self.NA(document.Sifra)]})
#        docDF["Naziv"] = [self.NA(document.Naziv)]
#        docDF["Skupina"] = ["/"]
#        docDF["Opis"] = [self.NA(document.OpisIzdelka)]
#        docDF["Sestavine"] = [self.NA(document.Sestavine)]
#        docDF["Izgled"] = [self.NA(document.Izgled)]
#        docDF["Okus In Vonj"] = [self.NA(document.Vonj)]
#        docDF = self.setMIKROBIOLOSKE(docDF,document)
#        docDF = self.setFIZIKALNO_KEMIJSKE_ZAHTEVE(docDF,document)
#        docDF["Zakonodaja"] = [self.NA(document.Zakonodaja)]
#        
#        
#        
#        print(docDF.columns)
#        if self.dataframe is not None:
#            self.dataframe = pd.concat([self.dataframe,docDF],axis=0,ignore_index=True)
#            self.dataframe = self.dataframe.reindex_axis(self.index,axis=1)
#        else:
#            self.dataframe = docDF
#    
#    def setMIKROBIOLOSKE(self,documentDF,document):
#        assert isinstance(document,parseXML.Document)
#        if document.MikrobiloskeZahteve:
#            for entry in document.MikrobiloskeZahteve:
#                if entry not in self.index:
#                    self.index = self.index.append(pd.Index([entry]))
#                documentDF[entry] = [document.MikrobiloskeZahteve[entry]]        
#            return documentDF
#        else:
#            return documentDF
#    
#    def setFIZIKALNO_KEMIJSKE_ZAHTEVE(self,documentDF,document):
#        assert isinstance(document,parseXML.Document)
#        if document.FizikalnoKemijskeZahteve:
#            for entry in document.FizikalnoKemijskeZahteve:
#                if entry not in self.index:
#                    self.index = self.index.append(pd.Index([entry]))
#                documentDF[entry] = [document.FizikalnoKemijskeZahteve[entry]]
#            return documentDF
#        else:
#            return documentDF
##    def setHRANILNA_VREDNOST(self,documentDF,document):
##        assert isinstance(document,parseXML.Document)
##        
##        if document.HranilnaVrednost:
##            
##    
#    def write(self,path):
#        writer = pd.ExcelWriter(path,engine="openpyxl")
#        self.dataframe.to_excel(writer, index=False)
#        writer.save()
#        
#    def NA(self,val):
#        if val:
#            return val
#        else:
#            return "NA"