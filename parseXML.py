# -*- coding: utf-8 -*-
import os
from bs4 import BeautifulSoup
import re
from pandas import DataFrame
import pandas as pd
import numpy as np




class Document():
    
    DocType = "1: Normal Tabled"
    
    def __init__(self,doc_path):
        """
        Provide a XML document that you want to parse, and a type ofdocument (table or text)
        example use:\n doc = Document("./DocData/SP 40408 Bio keksi pomaranča 150 g.xml","table")
        """
        self.Markers = {"Datum izdaje":re.compile("datum izdaje",re.IGNORECASE),
                        "opis_izdelka":re.compile("OPIS IZDELKA",re.IGNORECASE),
                        "sestavine":re.compile("SESTAVINE",re.IGNORECASE),
#                        "neto_kolicina":re.compile("neto količina",re.IGNORECASE),
                        "aroma":re.compile("aroma",re.IGNORECASE),
                        "videz":re.compile("videz",re.IGNORECASE),
                        "zakonodaja":re.compile("zakonodaja",re.IGNORECASE),
                        "mikrobioloske_zahteve":re.compile("mikrobiološke zahteve",re.IGNORECASE),
                        "fizikalno_kemijske_zahteve":re.compile("FIZIKALNO KEMIJSKE ZAHTEVE",re.IGNORECASE),
                        "hranilna_vrednost":re.compile("(.*)HRANILNA VREDNOST",re.IGNORECASE),
                        "aktivne_učinkovine":re.compile("tabela|vsebnost aktivnih komponent",re.IGNORECASE),
                        "senzoricne_zahteve":re.compile("senzorične zahteve",re.IGNORECASE),
                        "izdelal":re.compile("izdelal",re.IGNORECASE),
                        "pakiranje":re.compile("pakiranje",re.IGNORECASE)}
        self.doc_name = doc_path
        self.document = open(doc_path,"rb")
        self.doc_soup = BeautifulSoup(self.document,'html.parser')
        self.rows = None        
        self.textEntries = self.findAllTextEntries(self.doc_soup)
        
        self.textByRow = self.findRows()      
        self._HranilnaVrednostTemplate_ = None
        self.Naziv = None
        self.Sifra = None
        self.HranilnaVrednost = None
        self.MikrobiloskeZahteve = None
        self.FizikalnoKemijskeZahteve = None
        self.AktivneUcinkovine = None
        self.Pakiranje = None
        self.Zakonodaja = None
        self.DatumIzdaje = self.FindDatumIzdaje()
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
        self.HEADER_Dataframes = self.HEADER_PrepareDataFrames()
    
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
        txtEntries = soup.find_all("td")#(attrs={"lang":"sl-SI"})
        txtEntries = [x  for x in txtEntries if x.text != "\n"]
        txtEntries = [re.sub("[\t\n]"," ",x.text) for x in txtEntries]
        txtEntries = [re.sub(" +"," ",x) for x in txtEntries]
        txtEntries = [x.rstrip() for x in txtEntries]
        txtEntries = [x.lstrip() for x in txtEntries]
        return txtEntries
    
#    def findRowText(self):
#        """Extracts rows columns and values"""
#        rows = self.doc_soup.find_all("tr")
#        text_by_row = []
#        for row in rows:
#            tx = self.findAllTextEntries(row)
#            text_by_row.append(tx)
#        return text_by_row
    
    def findRows(self):
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
        if len(self.textByRow) > 0:
            text = " ".join(self.textByRow[0])
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
            
    def FindDatumIzdaje(self):
        for row in self.textByRow:
            for item in row:
                if bool(self.Markers["Datum izdaje"].match(item)):
                    return item
        return None
    
    def FindSimple(self,pattern):
        matches = []
        for row in self.textByRow:            
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
        for row in self.textByRow:
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
 
    
    #Processing sections and extracting values
    
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
            print(values)
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
        split = re.compile("((?:< *[0-9]*|neg.)(?:\.*|,*)[0-9]*)((?: *)(?:\/|cfu\/|CFU\/)(?: *)(?:[A-z]|(?:[0-9]*,*[0-9]* *[A-z]*)))",re.IGNORECASE)
        valRE = re.compile("^(neg.|<* *[0-9]+(?:,|\.)*[0-9]*)",re.IGNORECASE)
        unitRE = re.compile("(?:[A-Za-z]{3})* *(?:\/)(?:[0-9]*(?:,|\.)*[0-9]* *[A-Za-z]*)",re.IGNORECASE)
        
        for entry in mik_zaht:
#            print(entry)
            bact = entry[0]
            val = re.search(valRE,entry[1])
            un = re.search(unitRE,entry[1])
#            print(val,un)
#            value = re.match()
#            print(mik_zaht)
#            print(entry[1])
            if val:
                value = val.group(0)
            else:
                value = "#MV#"
            if un:
                unit = un.group(0)
            else:
                unit = "#MU#"
#            match = re.match(split,entry[1])
#            val = self.StandardizeFormat(match.group(1))
#            enota = self.StandardizeFormat(match.group(2))
            pathogens[bact] = [value,unit]
            
        self.MikrobiloskeZahteve = pathogens
        
        return pathogens
    
    def ProcessSection_FIZIKALNO_KEMIJSKE_ZAHTEVE(self):
        if "fizikalno_kemijske_zahteve" in self.Sections:
            fiz_kem_zaht = self.Sections["fizikalno_kemijske_zahteve"]        
        else:
            return None
        zahteve = {}
        averageRE = re.compile("(^[0-9]+(?:,|\.)*[0-9]*)",re.IGNORECASE)
        unitRE = re.compile("([^ 0-9]*\/[^ 0-9]*|%)",re.IGNORECASE)        
        minmaxOklepaj = re.compile("( *[0-9]*(?:,|\.)*[0-9]*) *(?:–|-)( *[0-9]*(?:,|\.)*[0-9]*)",re.IGNORECASE)
        minExplicit = re.compile("(?:min\. *)([0-9]*(?:,|\.)*[0-9]*)",re.IGNORECASE)
        maxExplicit = re.compile("(?:max\. *)([0-9]*(?:,|\.)*[0-9]*)",re.IGNORECASE)
        maxLogical = re.compile("(?:≤|<) *([0-9]*(?:,|\.)*[0-9]*)",re.IGNORECASE)
        for entry in fiz_kem_zaht:
            if entry and entry[0] != "/":
                val = entry[1]
                average = re.search(averageRE,val)
                unit = re.search(unitRE,val)
                minMAX = re.search(minmaxOklepaj,val)
                minExp = re.search(minExplicit,val)
                maxExp = re.search(maxExplicit,val)
                maxL = re.search(maxLogical,val)
                
                valTemplate = {"min":None,"max":None,"average":None,"unit":None}                
                if average:
                    valTemplate["average"] = average.group(1)
                if unit:
                    valTemplate["unit"] = unit.group(0)
                if minMAX:
                    valTemplate["min"] = minMAX.group(1)
                    valTemplate["max"] = minMAX.group(2)

                if minExp:
                    valTemplate["min"] = minExp.group(1)
                if maxExp:
                    valTemplate["max"] = maxExp.group(1)
                if maxL:
                    valTemplate["max"] = maxL.group(1)
                    
                measure = entry[0]
                zahteve[measure] = valTemplate

        self.FizikalnoKemijskeZahteve = zahteve
#        print(zahteve)
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
        
            aktivne_uc["[akt] " + ucinkovina] = values
        self.AktivneUcinkovine = aktivne_uc
        return aktivne_uc
    
    
    
    # Preparation of data frames for individual sections
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
                columns.append(entry+" enote")
                values.append(self.MikrobiloskeZahteve[entry][0])
                values.append(self.MikrobiloskeZahteve[entry][1])
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
#                print("#############################################3")
#                print(self.AktivneUcinkovine[entry])
#                print(self.Sections)
#                print(self.textByRow)
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
#                    print(hv["mascobe"])
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
    
    
    # Preparing PRE data frame format for new output format with units in a header
    def HEADER_PrepareDataFrames(self):
        dataframes = {}
        dataframes["Šifra"] = DataFrame({"Šifra":[self.Sifra]})
        dataframes["Naziv"] = DataFrame({"Naziv":[self.Naziv]})
        dataframes["Skupina"] = DataFrame({"Skupina":["/"]})
        dataframes["Opis"] = DataFrame({"Opis":[self.OpisIzdelka]})
        dataframes["Sestavine"] = DataFrame({"Sestavine":[self.Sestavine]})
        dataframes["Izgled"] = DataFrame({"Izgled":[self.Izgled]})
        dataframes["Okus In Vonj"] = DataFrame({"Okus in Vonj":[self.Vonj]})
        dataframes["Zakonodaja"] = DataFrame({"Zakonodaja":[self.Zakonodaja]})
        dataframes["Mikrobiološke Zahteve"] = self.HEADER_DFMikrobioloske()
        dataframes["Fizikalno Kemijske Zahteve"] = self.HEADER_DFfizikalno_kemijske()
        dataframes["Hranilna Vrednost"] = self.HEADER_DFhranilna_vrednost()
        dataframes["Aktivne učinkovine"] = self.HEADER_DFaktivne_ucinkovine()
        dataframes["Pakiranje"] = self.DFpakiranje()        
        return dataframes

    def HEADER_DFfizikalno_kemijske(self):
        if self.FizikalnoKemijskeZahteve:
            columns = []
            values = []
            for entry in self.FizikalnoKemijskeZahteve:
                unit = self.FizikalnoKemijskeZahteve[entry]["unit"]
                Min = self.FizikalnoKemijskeZahteve[entry]["min"]
                Max = self.FizikalnoKemijskeZahteve[entry]["max"]
                aver = self.FizikalnoKemijskeZahteve[entry]["average"]
                columns.append("[average] "+ entry + " " + "(" + self.NoneToStr(unit) +")")
                columns.append("[min] "+ entry + " " + "(" + self.NoneToStr(unit) +")")
                columns.append("[max] "+ entry + " " + "(" + self.NoneToStr(unit) +")")
                values.append(aver)
                values.append(Min)
                values.append(Max)
            return DataFrame([values],columns=columns)
        else:
            return DataFrame([np.NaN])

    def HEADER_DFMikrobioloske(self):
        if self.MikrobiloskeZahteve:
            columns = []
            values = []
            for entry in self.MikrobiloskeZahteve:
                unit = self.MikrobiloskeZahteve[entry][1]
                value = self.MikrobiloskeZahteve[entry][0]
                columns.append(entry + " " + "(" + self.NoneToStr(unit) +")")
                values.append(value)
            return DataFrame([values],columns=columns)
        else:
            return DataFrame([np.NaN])
    
    def HEADER_DFaktivne_ucinkovine(self):
        if self.AktivneUcinkovine:
            columns = []
            values = []
            for entry in self.AktivneUcinkovine:
                unit = self.StandardizeFormat(self.AktivneUcinkovine[entry][0][1])
                value =  self.StandardizeFormat(self.AktivneUcinkovine[entry][0][0])
                columns.append(entry + " " + "(" + unit +")")
                values.append(value)

                
            return DataFrame([values],columns=columns)
        else:
            return DataFrame([np.NaN])
    
    def HEADER_DFhranilna_vrednost(self):
        if self.HranilnaVrednost:
            hv = self.HranilnaVrednost
            columns = []
            values = []
            for ele in hv:
                if ele == "en_vrednost":
                    valueKJ = hv["en_vrednost"][0][0] 
                    unitKJ = hv["en_vrednost"][0][1]
                    valueKACAl = hv["en_vrednost"][1][0]
                    unitKACAL = hv["en_vrednost"][1][1]
                    columns.append("Energijska vrednost" +" "+ "(" + self.NoneToStr(unitKJ) +")")
                    columns.append("Energijska vrednost" +" "+ "(" + self.NoneToStr(unitKACAL) +")")
                    values.append(valueKJ)
                    values.append(valueKACAl)
                elif ele == "mascobe":
                    valueNorm = hv["mascobe"][0][0] 
                    unitNorm = hv["mascobe"][0][1]
                    valueNas = hv["mascobe"][1][0]
                    unitNas = hv["mascobe"][1][1]
                    columns.append("Maščobe" + " " + "(" + self.NoneToStr(unitNorm) +")")
                    columns.append("Nasičene M." + " " + "(" + self.NoneToStr(unitNas) +")")
                    values.append(valueNorm)
                    values.append(valueNas)

                elif ele == "oglikovi hidrati":
                    valueOh = hv["oglikovi hidrati"][0][0]
                    unitOh = hv["oglikovi hidrati"][0][1]
                    valueSladkor = hv["oglikovi hidrati"][1][0]
                    unitSladkor = hv["oglikovi hidrati"][1][1]
                    columns.append("Ogljikovi hidrati" + " " + "(" + self.NoneToStr(unitOh) +")")
                    columns.append("Sladkorji"+ " " + "(" + self.NoneToStr(unitSladkor) +")")
                    values.append(valueOh)
                    values.append(valueSladkor)
                elif ele == "vlaknine":
                    value = hv["vlaknine"][0][0]
                    unit = hv["vlaknine"][0][1]
                    columns.append("Prehranske vlaknine"+ " " + "(" + self.NoneToStr(unit) +")")
                    values.append(value)
                elif ele == "beljakonvine":
                    value = hv["beljakonvine"][0][0]
                    unit = hv["beljakonvine"][0][1]
                    columns.append("Beljakovine" + " " + "(" + self.NoneToStr(unit) +")")
                    values.append(value)
                elif ele == "sol":
                    value = hv["sol"][0][0]
                    unit = hv["sol"][0][1]
                    columns.append("Sol" + " " + "(" + self.NoneToStr(unit) +")")
                    values.append(value)
            return DataFrame([values],columns=columns)
        else:
            return DataFrame([np.NaN])
        
    
    # Utility functions from here on    
    def CountNONE(self):
        values= [self.Naziv,self.Sifra,self.HranilnaVrednost,self.MikrobiloskeZahteve,
                 self.FizikalnoKemijskeZahteve,self.Pakiranje,self.Zakonodaja,self.Sestavine,
                 self.OpisIzdelka,self.Vonj,self.Izgled,self.DatumIzdaje]        
        count = 0
        for i in values:
            if not(i):
                count += 1
        return count
    
    def StandardizeFormat(self,val):
        if val == "neg.":
            return "0"
        else:
            val = val.lower()
            val = val.replace(" ","")
            val = val.replace("cfu","").lstrip().rstrip()
            return val
        
    def NoneToStr(self,val):
        if val == None:
            return "Missing"
        else:
            return val

# External utility functions  
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
    


        











