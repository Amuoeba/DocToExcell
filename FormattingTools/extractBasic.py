# -*- coding: utf-8 -
from Medex.parseHTML import DocumentHTML
from FormattingTools import markers as markers
from FormattingTools.attribute import Attribute as  A
import re

def opisIzdelka(rows):
    m = markers.EXTRACTION_MARKERS["Opis izdelka"]
    for row in rows:
        if bool(re.search(m,row[0])):
            return row[1]
    return None

def sestavine(rows):
    m = markers.EXTRACTION_MARKERS["Sestavine"]
    for row in rows:
        if bool(re.search(m,row[0])):
            return row[1]
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
    return senzorika