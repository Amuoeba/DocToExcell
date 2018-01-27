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
#                        "neto_kolicina":re.compile("neto količina",re.IGNORECASE),
                        "aroma":re.compile("aroma",re.IGNORECASE),
                        "videz":re.compile("videz",re.IGNORECASE),
                        "zakonodaja":re.compile("zakonodaja",re.IGNORECASE),
                        "mikrobioloske_zahteve":re.compile("mikrobiološke zahteve",re.IGNORECASE),
                        "fizikalno_kemijske_zahteve":re.compile("FIZIKALNO KEMIJSKE ZAHTEVE",re.IGNORECASE),
                        "hranilna_vrednost":re.compile("(.*)HRANILNA VREDNOST",re.IGNORECASE),
                        "aktivne_učinkovine":re.compile("vsebnost|tabela",re.IGNORECASE),
                        "senzoricne_zahteve":re.compile("senzorične zahteve",re.IGNORECASE),
                        "izdelal":re.compile("izdelal",re.IGNORECASE),
                        "pakiranje":re.compile("pakiranje",re.IGNORECASE)}
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
#        self.NetoKolicina = self.FindSimple(self.Markers["neto_kolicina"])
        self.Aroma = self.FindSimple(self.Markers["aroma"])
        self.Videz = self.FindSimple(self.Markers["videz"])
        self.Zakonodaja = self.FindSimple(self.Markers["zakonodaja"])
        self.Sections = self.FindSections()        
        self.FindNazivSifra()
        self._HranilnaVrednostTemplate_ = None
        self.HranilnaVrednost = None
        self.MikrobiloskeZahteve = None
        self.ProcessSection_HRANILNA_VREDNOST()
        self.ProcessSection_MIKROBIOLOSKE_ZAHTEVE()
        
   
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
                section.append(row[1:])
            else:
                section.append(row)
                
            global_identifier = local_identifier
        return global_sections
 
    
#    def ProcessSection_PAKIRANJE(self):
    def ProcessSection_HRANILNA_VREDNOST(self):
        markers = {"en_vrednost":re.compile("energijska vrednost",re.IGNORECASE),
                   "mascobe":re.compile("maščobe",re.IGNORECASE),
                   "oglikovi hidrati":re.compile("ogljikovi hidrati",re.IGNORECASE),
                   "vlaknine":re.compile(".*vlaknine",re.IGNORECASE),
                   "beljakonvine":re.compile("beljakovine",re.IGNORECASE),
                   "sol":re.compile("sol",re.IGNORECASE)}
        
        if "hranilna_vrednost" in self.Sections:
            hran_vrednosti = self.Sections["hranilna_vrednost"]
        else:
            return None        
        data = []
        for entry in hran_vrednosti:
            values = []
            v = re.compile("([0-9]+,[0-9]+)(?: *)([a-z]*)|([0-9]+)(?: *)([a-z]*)",re.IGNORECASE)
            hranilo = None            
            for i in entry:  
                for m in markers:
                    marker = markers[m]
                    if  bool(marker.match(i)):                        
                        hranilo  = m
            for i in entry:
                vrednosti = re.findall(v,i)
                if vrednosti != []:
                    values = values + vrednosti            
 
            values = list(map(getMatchedGroup,values))
            data.append({hranilo:values})
            
        self._HranilnaVrednostTemplate_ = data[0]
        self.HranilnaVrednost = data[1:]
        return data[0],data[1:]
    
    
    def ProcessSection_MIKROBIOLOSKE_ZAHTEVE(self):
        if "mikrobioloske_zahteve" in self.Sections:
            mik_zaht = self.Sections["mikrobioloske_zahteve"]
        
        else:
            return None
        pathogens = []
        for entry in mik_zaht:
            bact = entry[0]
            pathogens.append({bact:entry[1]})
            
        self.MikrobiloskeZahteve = pathogens
        return pathogens
#        def defineDataShape():
            
#        section = self.Sections("hranilna_vrednost")
#        perRegex = re.compile("([a-z]+) *([0-9]{3,}) *([a-z]*)",re.IGNORECASE)
#        perEnota = "g"
#        perKolicina = 100
#        for row in section:
#            for ele in row:
#                match = perRegex.match(ele)
#                if bool(match):
#                    perKolicina=match.group(2)
#                    perEnota = match.group(3)
#        perRegex2 = re.compile("([A-Za-z])+ (priporo[a-ž]* dnevno količino|porc[a-ž]*).*?([0-9] ?g)",re.IGNORECASE)
#        perEnota2 = None
#        perKolicina2 = None
#        for row in section:
#            for ele in row:
#                match = perRegex2.match(ele)
#                if bool(match):
#                    perKolicina2 = match.group(3)
#                    perEnota2 = match.group(5)
#        perRegex3 = re.compile("(% \bPV\b|%pv\b|% \bpv\b|\bpv\b)",re.IGNORECASE)
#        PV = False
#        for ele in section[0]:
#            if bool(perRegex3.match(ele)):
#                PV = True
        
        
                
        
        
        
        
        
    
def botomUp(textele):
    if textele:
        if textele.name == "tr":
            return textele
        else:
            return botomUp(textele.parent)
    else:
        return None

def getMatchedGroup(tup):
    matched = []
    for i in tup:
        if i != '':
            matched.append(i)    
    return matched
    

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