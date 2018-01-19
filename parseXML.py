# -*- coding: utf-8 -*-
import os
from bs4 import BeautifulSoup
import re





class Document():
    def __init__(self,doc_path,tip):
        """
        Provide a XML document that you want to parse, and a type ofdocument (table or text)
        example use:\n doc = Document("./DocData/SP 40408 Bio keksi pomaranča 150 g.xml","table")
        """
        self.doc_name = doc_path
        self.document = open(doc_path,"rb")
        self.doc_soup = BeautifulSoup(self.document,"html")        
        self.textEntries = self.findAllTextEntries(self.doc_soup)
        self.textByRow = self.findRowText()
   
    def findAllTextEntries(self,soup):
        """Extract just text entries sequentially"""
        
#        for doc in documents:
#            soup = doc.doc_soup
#            print("################" + doc.doc_name)
#            for i in soup.find_all("p",{"lang":"sl-SI"}):
#                if i.text != "\n":
#                    text = i.text
#                    text = re.sub("[\t\n]"," ",text)
#                    text = re.sub(" +"," ",text)
#                    print(text)
        
        txtEntries = soup.find_all(attrs={"lang":"sl-SI"})
        txtEntries = [x  for x in txtEntries if x.text != "\n"]
        txtEntries = [re.sub("[\t\n]"," ",x.text) for x in txtEntries]
        txtEntries = [re.sub(" +"," ",x) for x in txtEntries]
        return txtEntries
    
    def findRowText(self):
        """Extracts rows columns and values"""
        rows = self.doc_soup.find_all("tr")
        text_by_row = []
        for row in rows:
            tx = self.findAllTextEntries(row)
            text_by_row.append(tx)
        return text_by_row

    
   
#    def preety_print(self):
#        """Prints the extracted features by row"""
#        for row in self.rows:
#            assert isinstance(row,Row)
#            row_st = []
#            for column in row.columns:
#                assert isinstance(column,Column)
#                col_st = column.to_string()
#                col_st = " ".join(col_st)
#                row_st.append(col_st)
#            print(row_st)

#class Row():
#    def __init__(self,columns):
#        self.columns = columns
#    
#    def set_new_columns(self,colList):
#        self.columns = colList
#        
#class Column():
#    def __init__(self,entries):
#        self.entries = entries
#        
#    def to_string(self):
#        string = []
#        for item in self.entries:
#            t=item.text
#            string.append(t)
#        
#        return string