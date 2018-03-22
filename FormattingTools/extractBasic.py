 # -*- coding: utf-8 -
from Medex.parseHTML import DocumentHTML
from FormattingTools import markers as markers
from FormattingTools.helper_classes import Attribute as  A
from FormattingTools.helper_classes import RowFormat as RowFormat
from FormattingTools import aux_tools
import re

def opisIzdelka(rows):
    m = markers.EXTRACTION_MARKERS["Opis izdelka"]
    for row in rows:
        if bool(re.search(m,row[0])):
            return A("Opis izdelka",value=row[1])
    return None

def sestavine(rows):
    m = markers.EXTRACTION_MARKERS["Sestavine"]
    for row in rows:
        if bool(re.search(m,row[0])):
            return A("Sestavine",row[1])
    return None

def senzorika(rows):
    m = markers.EXTRACTION_MARKERS["Senzorične zahteve"]
    senzorika = []
    for row in rows:
        if len(row) > 1:
            if bool(re.search(m,row[0])):
                attribute = row[1]
                value = row[2]
                senzorika.append(A(attribute,value))
    
    if senzorika == []:
        return None
    return senzorika

def microbiological(rows):
#    for i in rows:
#        print(i)
    m = markers.EXTRACTION_MARKERS["Mikrobiološke zahteve"]
    microbio = []
    for row in rows:
        if bool(re.search(m,row[0])):
            catRow = RowFormat(row)
#            microbio.append((catRow.catRow,catRow.raw_row))            
            if catRow.no_entries > 2:
                valRe = markers.MICROBIOLOGICAL["Value"]
                unitRe = markers.MICROBIOLOGICAL["Unit"]           
                bact = catRow.raw_row[1]
                Min = catRow.catRow[2]["min"]
                Max = catRow.catRow[2]["max"]
                if not Min and not Max:
                    value = re.search(valRe,row[2]).group(1)
                else:
                    value = None
                unit = re.search(unitRe,row[2])
                
                if value:
                    value= value.lower().rstrip().lstrip()
                    if bool(re.search(markers.REPLACERS["neg."],value)):
                        value = "0"                        
                if unit:
                    unit = unit.group(0)
                    unit = unit.lower().lstrip().rstrip()
                
#                print(value)
                MicroEntry = A(bact,value=value,Max=Max,Min=Min,unit=unit)            
                microbio.append(MicroEntry)      
    if microbio == []:
        return None
    return microbio

def fizikalnoKemijske(rows):
    m = markers.EXTRACTION_MARKERS["Fizikalno kemijske zahteve"]
    fizKem = []
    for row in rows:
        if bool(re.search(m,row[0])):
            averageValRE = markers.FIZKEM["Value"]
            vodilniCvetniPrahRE = markers.FIZKEM["Vodilni cvetni prahovi"]
            catRow = RowFormat(row)
#            fizKem.append((catRow,catRow.raw_row))
            
            if catRow.no_entries ==3:
                if not catRow.catRow[1]["unit"] and not catRow.catRow[1]["max"] and not catRow.catRow[1]["min"]:
                    name = catRow.raw_row[1]
                else:
                    name = "Wrong entry"
                
                unit = catRow.catRow[2]["unit"]
                Min = catRow.catRow[2]["min"]
                Max = catRow.catRow[2]["max"]
                
                value = re.search(averageValRE,catRow.raw_row[2])
                if bool(value):
                    value = [value.group(0)]
                else:
                    value = None
                if value == Min or value == Max:
                    value = None
                
                if value == None and Max == None and unit == None and Min == None or bool(re.search(vodilniCvetniPrahRE,name)):
                    value = catRow.raw_row[2]
                
                FizKemEntry = A(name,value=value,Max=Max,Min=Min,unit=unit)                
                fizKem.append(FizKemEntry)
                
    if fizKem == []:
        return None
    return fizKem

def hranilnaVrednost(rows):
    m = markers.EXTRACTION_MARKERS["Hranilna vrednost"]
    hvRows = [x for x in rows if bool(re.search(m,x[0]))]
    
    hranilnaVrednost = []
    
    if hvRows != []:
        headerRow = hvRows[0]
        catHeader = RowFormat(headerRow)
        per = []
#        print(headerRow)
        for entry in headerRow:
            mPer = markers.HRANILNA["Per"]
            matches = re.findall(mPer,entry)
            if matches != []:
                per = per + matches        
        per = aux_tools.cleanPer(per)
        per = per[:2]
        
        for row in hvRows[1:]:
            catRow = RowFormat(row)            
            if catRow.no_entries > 2:
                split = len(per) - (catRow.no_entries -2)                
                if split > 0:
                    catRow.splitRow(split)         
                name = row[1]
                for entry in enumerate(catRow.catRow[2:]):
                    ind = entry[0]
                    entry = entry[1]
                    if len(per)>ind:
                        p = per[ind]
                    else:
                        p = None
                    value = entry["number"]
                    Max = entry["max"]
                    Min = entry["min"]
                    unit = entry["unit"]
                    HranEntry = A(name,value=value,Min=Min,Max=Max,unit=unit,per=p)
                    
                    hranilnaVrednost.append(HranEntry)
    else:
        return None
            
    if hranilnaVrednost == []:
        return None
    return hranilnaVrednost

def aktivneUcinkovine(rows):
    m = markers.EXTRACTION_MARKERS["Aktivne učinkovine"]
    aktivneUcinkovine = []
    
    headerRow = None
    catRows = []
    for row in rows:
        if bool(re.search(m,row[0])):
            catRow = RowFormat(row)
            catRows.append(catRow)
            if catRow.header:
                headerRow = catRow            
#            aktivneUcinkovine.append(catRow)    
    per = []
    if headerRow:
        for entry in headerRow.raw_row:
            mPer = markers.AKTIVNE["Per"]
            matches = re.findall(mPer,entry)
            if matches != []:
                per = per + matches        
        per = aux_tools.cleanPer(per)
        per = per[:2]
    
    for row in catRows:
        if row.no_entries > 2 and not row.header:
            name = row.raw_row[1]
            for entry in row.catRow[2:]:
                value = entry["number"]
                Max = entry["max"]
                Min = entry["min"]
                unit = entry["unit"]
                AktEntry = A(name,value=value,Min=Min,Max=Max,unit=unit,per=None)
                aktivneUcinkovine.append(AktEntry)    
    if aktivneUcinkovine == []:
        return None    
    return aktivneUcinkovine
    

def pakiranje(rows):
    m = markers.EXTRACTION_MARKERS["Pakiranje"]
    pakiranje = []
    
    for row in rows:
        if bool(re.search(m,row[0])) and len(row) > 1:
            for ele in enumerate(row):
                for marker in markers.PAKIRANJE:
                    reg = markers.PAKIRANJE[marker]
                    if bool(re.match(reg,ele[1])):                     
                        name = marker
                        if (len(row)-1) >= (ele[0]+1):
                            value = row[ele[0]+1]
                        else:
                            value = "/"
                        pakiranjeEntry = A(name,value=value)
                        pakiranje.append(pakiranjeEntry)    
    if pakiranje == []:
        return None    
    return pakiranje

def zakonodaja(rows):
    m = markers.EXTRACTION_MARKERS["Zakonodaja"]
    zakonodaja = []
    
    auxRows = []
    for row in rows:
        if bool(re.search(m,row[0])) and len(row) > 1:
            auxRows.append(row)
    
    if auxRows != []:
        name = "Zkonodaja"
        value = auxRows[0][-1]
        zakonodajaEntry = A(name,value=value)
        zakonodaja.append(zakonodajaEntry)
    if zakonodaja == []:
        return None
    return zakonodaja
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        