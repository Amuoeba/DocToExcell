# -*- coding: utf-8 -*-
from parseXML import Document
import re
from bs4 import BeautifulSoup

class DocumentUnstructured(Document):
    DocType = "2: Only textual"
    
    def __init__(self,doc_path):
        super().__init__(doc_path)
        self.MarkersSpecific = {"Naziv":re.compile("ime izdelk",re.IGNORECASE),
                                "Sestava materiala":re.compile("sestava mat",re.IGNORECASE),
                                "Skladiščenje":re.compile("pogoji skla",re.IGNORECASE),
                                "Dobavitelj":re.compile("dobavitelj",re.IGNORECASE)}
        self.rows = self.FindRows(self.doc_soup)
        self.Attributes = {}
        self.ProcessBasic()
        
    
    def FindRows(self,soup):
        """Extract just text entries sequentially"""
        txtEntries = soup.find_all("p")#(attrs={"lang":"sl-SI"})
        txtEntries = [x  for x in txtEntries if x.text != "\n"]
        txtEntries = [re.sub("[\t\n]"," ",x.text) for x in txtEntries]
        txtEntries = [re.sub(" +"," ",x) for x in txtEntries]
        txtEntries = [x.rstrip() for x in txtEntries]
        txtEntries = [x.lstrip() for x in txtEntries]        
        return txtEntries
    

    
    def ProcessBasic(self):
        exp = re.compile("(?:.*?):(.*)",re.IGNORECASE)
        for row in self.rows:
            for marker in self.MarkersSpecific:
                if bool(re.match(self.MarkersSpecific[marker],row)):
                    m = re.match(exp,row)
                    value = m.group(1)
                    self.Attributes[marker] = value
        return None
            