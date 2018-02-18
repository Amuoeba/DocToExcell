# -*- coding: utf-8 -*-
import os
from bs4 import BeautifulSoup
import re
from pandas import DataFrame
import pandas as pd
import numpy as np



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
        self._HranilnaVrednostTemplate_ = None
        self.Naziv = None
        self.Sifra = None
        self.HranilnaVrednost = None
        self.MikrobiloskeZahteve = None
        self.FizikalnoKemijskeZahteve = None
        self.AktivneUcinkovine = None
        self.Pakiranje = None
        self.Zakonodaja = None
        self.Sestavine = self.FindSimple(self.Markers["sestavine"])
        self.OpisIzdelka = self.FindSimple(self.Markers["opis_izdelka"])
        self.Vonj = self.FindSimple(self.Markers["aroma"])
        self.Izgled = self.FindSimple(self.Markers["videz"])        
        self.Sections = self.FindSections()        
        self.FindNazivSifra()
        self.ProcessSection_HRANILNA_VREDNOST()
        self.ProcessSection_MIKROBIOLOSKE_ZAHTEVE()
        self.ProcessSection_FIZIKALNO_KEMIJSKE_ZAHTEVE()
        self.ProcessSection_PAKIRANJE()
        self.ProcessSection_ZAKONODAJA()
        self.ProcessSection_AKTIVNE_UCINKOVINE()
        self.Dataframes = self.PrepareDataFrames()
    
    def listAttributes(self):
        attrList = ["Naziv","Sifra","Izgled","Vonj","Zakonodaja","Sestavine","OpisIzdelka"]
        if self.HranilnaVrednost:
            for i in self.HranilnaVrednost:
                attrList.append(i)
        if self.MikrobiloskeZahteve:
            for i in self.MikrobiloskeZahteve:
                attrList.append(i)
        if self.FizikalnoKemijskeZahteve:
            for i in self.FizikalnoKemijskeZahteve:
                attrList.append(i)
        if self.Pakiranje:
            for i in self.Pakiranje:
                attrList.append(i)        
        return attrList
   
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
            return "".join(matches)
    
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
        data = {}
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
#            data.append({hranilo:values})
            data[hranilo] = values
            
        self._HranilnaVrednostTemplate_ = data[None]
        if None in data:
            del data[None]
        self.HranilnaVrednost = data
        return data
    
    
    def ProcessSection_MIKROBIOLOSKE_ZAHTEVE(self):
        if "mikrobioloske_zahteve" in self.Sections:
            mik_zaht = self.Sections["mikrobioloske_zahteve"]
        
        else:
            return None
        pathogens = {}
        for entry in mik_zaht:
            bact = entry[0]
            pathogens[bact] = entry[1]
            
        self.MikrobiloskeZahteve = pathogens
        return pathogens
    
    def ProcessSection_FIZIKALNO_KEMIJSKE_ZAHTEVE(self):
        if "fizikalno_kemijske_zahteve" in self.Sections:
            fiz_kem_zaht = self.Sections["fizikalno_kemijske_zahteve"]        
        else:
            return None
        zahteve = {}
        for entry in fiz_kem_zaht:
            if entry and entry[0] != "/":
                val = entry[0]
#                zahteve.append({val:entry[1]})
                zahteve[val] = entry[1]
#                print("val: ",val," entry: ",entry)
            
        self.FizikalnoKemijskeZahteve = zahteve
        return zahteve
        
    def ProcessSection_PAKIRANJE(self):
        markers = {"neto":re.compile("neto koli[a-ž]*?",re.IGNORECASE),
#                   "embalaža":re.compile("embalaža",re.IGNORECASE),
                   "tip MPE":re.compile("tip mpe",re.IGNORECASE),
                   "tip TP":re.compile("tip tp",re.IGNORECASE),
                   "tip KP":re.compile("tip kp",re.IGNORECASE),
                   "dimenzija MPE":re.compile("dime[a-ž]*? mpe",re.IGNORECASE),
                   "dimenzija TP":re.compile("dime[a-ž]*? tp",re.IGNORECASE),
                   "dimenzija KP":re.compile("dime[a-ž]*? kp",re.IGNORECASE),
                   "število MPE":re.compile("število mpe na",re.IGNORECASE),
                   "število plasti na paleti":re.compile("število plasti na pale",re.IGNORECASE),
                   "način transporta":re.compile("način transporta",re.IGNORECASE),
                   "način skladiščenja":re.compile("način skladiščenja",re.IGNORECASE),
                   "rok uporabe":re.compile("rok upo",re.IGNORECASE)}
        
        if "pakiranje" in self.Sections:
            pakiranje = self.Sections["pakiranje"]
        else:
            return None
        
        concat_pakiranje = []
        for i in pakiranje:
            concat_pakiranje = concat_pakiranje + i
        
        pakiranje_values = {}
        
        for ele in enumerate(concat_pakiranje):
            for marker in markers:
                m = markers[marker]
                if bool(re.match(m,ele[1])):
                    pakiranje_values[marker] = concat_pakiranje[ele[0]+1]
                    
        self.Pakiranje = pakiranje_values
        
        return  pakiranje_values
    
    def ProcessSection_ZAKONODAJA(self):
        if "zakonodaja" in self.Sections:
            zakonodaja = self.Sections["zakonodaja"]
        else:
            return None
        
        m = re.compile("zakonske zahteve",re.IGNORECASE)
        zakonodaja_concat = []
        for i in zakonodaja:
            zakonodaja_concat = zakonodaja_concat + i
        
        zakonodaja_concat = [x for x in zakonodaja_concat if not bool(re.match(m,x))]
        zakonodaja_concat = " ".join(zakonodaja_concat)
        self.Zakonodaja = zakonodaja_concat        
        return zakonodaja_concat
    
    def ProcessSection_AKTIVNE_UCINKOVINE(self):
        if "aktivne_učinkovine" in self.Sections:
            akt_uc = self.Sections["aktivne_učinkovine"]
        else:
            return None
        valRegex = re.compile("([0-9]+)(?: *)((?!\d)\w{1,3})|([0-9]+,[0-9]+)(?: *)((?!\d)\w{1,3})",re.IGNORECASE | re.UNICODE)
        
        aktivne_uc = {}
        
        for ele in akt_uc[1:-1]:
            ucinkovina = ele[0]
            values = []
            for v in ele[1:]:
                val = re.findall(valRegex,v)
                val = list(map(getMatchedGroup,val))
                values = values + val
        
            aktivne_uc[ucinkovina + "(akt)"] = values
        self.AktivneUcinkovine = aktivne_uc
        return aktivne_uc
    
    def PrepareDataFrames(self):
        dataframes = {}
        dataframes["Šifra"] = DataFrame({"Šifra":[self.Sifra]})
        dataframes["Naziv"] = DataFrame({"Naziv":[self.Naziv]})
        dataframes["Skupina"] = DataFrame({"Skupina":["/"]})
        dataframes["Opis"] = DataFrame({"Opis":[self.OpisIzdelka]})
        dataframes["Sestavine"] = DataFrame({"Sestavine":[self.Sestavine]})
        dataframes["Izgled"] = DataFrame({"Izgled":[self.Izgled]})
        dataframes["Okus In Vonj"] = DataFrame({"Okus in Vonj":[self.Vonj]})
        dataframes["Zakonodaja"] = DataFrame({"Zakonodaja":[self.Zakonodaja]})
        dataframes["Mikrobiološke Zahteve"] = self.DFmikrobioloske()
        dataframes["Fizikalno Kemijske Zahteve"] = self.DFfizikalno_kemijske()
        dataframes["Hranilna Vrednost"] = self.DFhranilna_vrednost()
        dataframes["Aktivne učinkovine"] = self.DFaktivne_ucinkovine()
        dataframes["Pakiranje"] = self.DFpakiranje()

        
        return dataframes
    
    
    def DFmikrobioloske(self):
        if self.MikrobiloskeZahteve:
            columns = []
            values = []
            for entry in self.MikrobiloskeZahteve:
                columns.append(entry)
                values.append(self.MikrobiloskeZahteve[entry])            
            return DataFrame([values],columns=columns)
        else:
            return DataFrame([np.NaN])
        
    
    def DFfizikalno_kemijske(self):
        if self.FizikalnoKemijskeZahteve:
            columns = []
            values = []
            for entry in self.FizikalnoKemijskeZahteve:
                columns.append(entry)
                values.append(self.FizikalnoKemijskeZahteve[entry])            
            return DataFrame([values],columns=columns)
        else:
            return DataFrame([np.NaN])
    
    def DFpakiranje(self):
        if self.Pakiranje:
            columns = []
            values = []
            for entry in self.Pakiranje:
                columns.append(entry)
                values.append(self.Pakiranje[entry])
            return DataFrame([values],columns=columns)
        else:
            return DataFrame([np.NaN])
    def DFaktivne_ucinkovine(self):
        if self.AktivneUcinkovine:
            columns = []
            values = []
            for entry in self.AktivneUcinkovine:
                columns.append(entry)
                columns.append(entry + "Enote")
                values.append(self.AktivneUcinkovine[entry][0][0])
                values.append(self.AktivneUcinkovine[entry][0][1])
            return DataFrame([values],columns=columns)
        else:
            return DataFrame([np.NaN])
        
    
    def DFhranilna_vrednost(self):
        if self.HranilnaVrednost:
            hv = self.HranilnaVrednost

            columns = []
            values = []
            for ele in hv:
                if ele == "en_vrednost":
                    columns.append("Energijska vrednost 1")
                    columns.append("ENV1 Enote")
                    columns.append("Energijska vrednost 2")
                    columns.append("ENV2 Enote")
                    values.append(hv["en_vrednost"][0][0])
                    values.append(hv["en_vrednost"][0][1])
                    values.append(hv["en_vrednost"][1][0])
                    values.append(hv["en_vrednost"][1][1])
                elif ele == "mascobe":
                    columns.append("Maščobe")
                    columns.append("M Enote")
                    columns.append("Nasičene")
                    columns.append("MN Enote")
                    values.append(hv["mascobe"][0][0])
                    values.append(hv["mascobe"][0][1])
                    values.append(hv["mascobe"][1][0])
                    values.append(hv["mascobe"][1][1])
                elif ele == "oglikovi hidrati":
                    columns.append("Ogljikovi hidrati")
                    columns.append("OH Enote")                    
                    columns.append("Sladkorji")
                    columns.append("S Enote")
                    values.append(hv["oglikovi hidrati"][0][0])
                    values.append(hv["oglikovi hidrati"][0][1])
                    values.append(hv["oglikovi hidrati"][1][0])
                    values.append(hv["oglikovi hidrati"][1][1])
                elif ele == "vlaknine":
                    columns.append("Prehranske vlaknine")
                    columns.append("PV Enote")
                    values.append(hv["vlaknine"][0][0])
                    values.append(hv["vlaknine"][0][1])
                elif ele == "beljakonvine":
                    columns.append("Beljakovine")
                    columns.append("B Enote")
                    values.append(hv["beljakonvine"][0][0])
                    values.append(hv["beljakonvine"][0][1])
                elif ele == "sol":
                    columns.append("Sol")
                    columns.append("Sol Enote")
                    values.append(hv["sol"][0][0])
                    values.append(hv["sol"][0][1])
            return DataFrame([values],columns=columns)
        else:
            return DataFrame([np.NaN])
            
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