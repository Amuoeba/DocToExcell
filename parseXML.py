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
        self.Markers = {"opis_izdelka":re.compile("OPIS IZDELKA",re.IGNORECASE),
                        "sestavine":re.compile("SESTAVINE",re.IGNORECASE),
                        "neto_kolicina":re.compile("neto količina",re.IGNORECASE),
                        "aroma":re.compile("aroma",re.IGNORECASE),
                        "videz":re.compile("videz",re.IGNORECASE),
                        "zakonodaja":re.compile("zakon(.*)",re.IGNORECASE),
                        "mikrobioloske_zahteve":re.compile("mikrobiološke zahteve",re.IGNORECASE),
                        "fizikalno_kemijske_zahteve":re.compile("FIZIKALNO KEMIJSKE ZAHTEVE",re.IGNORECASE),
                        "hranilna_vrednost":re.compile("(.*)HRANILNA VREDNOST",re.IGNORECASE)}
        self.doc_name = doc_path
        self.document = open(doc_path,"rb")
        self.doc_soup = BeautifulSoup(self.document,'html.parser')
        self.rows = None        
        self.textEntries = self.findAllTextEntries(self.doc_soup)
        self.textByRow = self.findRowText()
        self.textByRow1 = self.findRows1()
        self.Naziv = None
        self.Sifra = None
        self.OpisIzdelka = self.FindSimple(self.Markers["opis_izdelka"])
        self.Sestavine = self.FindSimple(self.Markers["sestavine"])
        self.NetoKolicina = self.FindSimple(self.Markers["neto_kolicina"])
        self.Aroma = self.FindSimple(self.Markers["aroma"])
        self.Videz = self.FindSimple(self.Markers["videz"])
        self.Zakonodaja = self.FindSimple(self.Markers["zakonodaja"])
        self.Sections = self.FindSections()        
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
        
        
        txtEntries = soup.find_all("td")#(attrs={"lang":"sl-SI"})
        txtEntries = [x  for x in txtEntries if x.text != "\n"]
        txtEntries = [re.sub("[\t\n]"," ",x.text) for x in txtEntries]
        txtEntries = [re.sub(" +"," ",x) for x in txtEntries]
        txtEntries = [x.rstrip() for x in txtEntries]
        txtEntries = [x.lstrip() for x in txtEntries]
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
        matches = []
        for row in self.textByRow1:
            
            for item in enumerate(row):
                if bool(pattern.match(item[1])):
                    match = row[item[0]+1:]
                    match=" ".join(match)
                    matches.append(match)
        
        if matches == []:
            return None
        else:
            return matches
    
    def FindSections(self):
        global_identifier = None
        local_identifier = None
        section = []
        global_sections = {}
        for row in self.textByRow1:
            first = row[0]
            for m in self.Markers:
                marker = self.Markers[m]
                if bool(marker.match(first)):
                    local_identifier = m
                
            if global_identifier != local_identifier:
                global_sections[global_identifier] = section
                section = []
                section.append(row)
            else:
                section.append(row)
                
            global_identifier = local_identifier
        return global_sections
 
    
    
    
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




class Section():
    def __init__(self,name,data):
        self.name = name
        self.data = data



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