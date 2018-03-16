 # -*- coding: utf-8 -
from Medex.parseHTML import DocumentHTML
from FormattingTools import markers as markers
from FormattingTools.helper_classes import Attribute as  A
from FormattingTools.helper_classes import RowFormat as RowFormat
import re

def opisIzdelka(rows):
    m = markers.EXTRACTION_MARKERS["Opis izdelka"]
    for row in rows:
        if bool(re.search(m,row[0])):
            return A("Opis  izdelka",row[1])
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
    hranilnaVrednost = []
    for row in rows:
        if bool(re.search(m,row[0])):
            count = 0
            for ele in row:
                c = len(re.findall(markers.HRANILNA["Na"],ele))
                count = count + c
            catRow = RowFormat(row)
            hranilnaVrednost.append((catRow,catRow.raw_row,count))                
    if hranilnaVrednost == []:
        return None
    return hranilnaVrednost