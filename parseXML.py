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
        self.doc_soup = BeautifulSoup(self.document,'html.parser')
        self.rows = None        
        self.textEntries = self.findAllTextEntries(self.doc_soup)
        self.textByRow = self.findRowText()
        self.textByRow1 = self.findRows1()
        self.Naziv = None
        self.Sifra = None
        self.OpisIzdelka = self.FindSimple("OPIS IZDELKA")
        self.Sestavine = self.FindSimple("SESTAVINE")
        self.NetoKolicina = self.FindSimple("NETO KOLIČINA")
        self.FindNazivSifra()
        
   
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
    
    def findRows1(self):
        txtEntries = self.doc_soup.find_all("font")#attrs={"lang":"sl-SI"})
        rows = []
        for ele in txtEntries:
            row = botomUp(ele)
            if row:
                rows.append(row)
        text_by_row = []
        aux = set()
        self.rows = rows
        for row in rows:
            tx = self.findAllTextEntries(row)
            aux_tx = str(tx)
            if aux_tx not in aux:
                text_by_row.append(tx)
                aux.add(aux_tx)
            
        return text_by_row

    def FindNazivSifra(self):
        text = " ".join(self.textByRow1[0])
        Rnaziv = re.compile("(?<=PROIZVODA )(.*)(?= Šifra)")
        Ršifra = re.compile("(?<=Šifra: )(.*)(?= Izdaja)")
        
        naziv = re.search(Rnaziv,text)
        sifra = re.search(Ršifra,text)
        
        if naziv:
            naziv = naziv.group(0)
            self.Naziv = naziv
        if sifra:
            sifra = sifra.group(0)
            self.Sifra = sifra
    
    def FindSimple(self,pattern):
        for row in self.textByRow1:
            for item in enumerate(row):
                if item[1] == pattern:
                    opis = row[item[0]+1:]
                    opis=" ".join(opis)
                    return opis       
        return None
 
    
    
    
def botomUp(textele):
    if textele:
        if textele.name == "tr":
            return textele
        else:
            return botomUp(textele.parent)
    else:
        return None
    

class RegExTable():
    def __init__(self):
        self.SecifikacijaProizvoda = re.compile("")
        


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