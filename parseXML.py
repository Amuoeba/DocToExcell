# -*- coding: utf-8 -*-
import os
from bs4 import BeautifulSoup





class Document():
    def __init__(self,doc_path,tip):
        """
        Provide a XML document that you want to parse, and a type ofdocument (table or text)
        example use:\n doc = Document("./DocData/SP 40408 Bio keksi pomaranča 150 g.xml","table")
        """
        self.doc_name = doc_path
        self.document = open(doc_path,"rb")
        self.doc_soup = BeautifulSoup(self.document,"xml")
        self.rows = self.findRowColumn()
        
    
    def findRowColumn(self):
        """Extracts rows columns and values"""
        rows = self.doc_soup.find_all("w:tr")
        
        rows_aug = []
        
        for row in rows:
            cols=row.find_all("w:tc")
            new = Row(cols)
            rows_aug.append(new)
            
        for row in rows_aug:
            assert isinstance(row,Row)
            colums_aug = []
            for column in row.columns:
                entries = column.find_all("w:t")
                new_c = Column(entries)
                colums_aug.append(new_c)
            row.set_new_columns(colums_aug)      
                
        return rows_aug
    
   
    def preety_print(self):
        """Prints the extracted features by row"""
        for row in self.rows:
            assert isinstance(row,Row)
            row_st = []
            for column in row.columns:
                assert isinstance(column,Column)
                col_st = column.to_string()
                col_st = " ".join(col_st)
                row_st.append(col_st)
            print(row_st)

class Row():
    def __init__(self,columns):
        self.columns = columns
    
    def set_new_columns(self,colList):
        self.columns = colList
        
class Column():
    def __init__(self,entries):
        self.entries = entries
        
    def to_string(self):
        string = []
        for item in self.entries:
            t=item.text
            string.append(t)
        
        return string