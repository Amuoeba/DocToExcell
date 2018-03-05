# -*- coding: utf-8 -*-
from parseXML import Document
import re
from datetime import datetime
from parseHTML import DocumentHTML
import FormattingTools.markers as markers


def GetDate(doc):
    assert isinstance(doc, DocumentHTML)
    dateRe = re.compile(".*?([0-9]*)\.([0-9]*)\.([0-9]*)",re.IGNORECASE)
    datumIzdaje = doc.DatumIzdaje
#    print(doc.doc_name)
    m = re.match(dateRe,datumIzdaje)
    
    date = datetime(int(m.group(3)),int(m.group(2)),int(m.group(1)))
    return date


def FindMostRecent(docList):
    """Finds most recent document in a set of documents that have same ID code"""
    docsBySifra = {}
    
    for doc in docList:
        assert isinstance(doc,DocumentHTML)
        if doc.Sifra not in docsBySifra:
            docsBySifra[doc.Sifra] = [doc]
        else:
            docsBySifra[doc.Sifra].append(doc)
    
    documents =[]    
    for sifra in docsBySifra:
        if len(docsBySifra[sifra]) > 1:
            maxDate = GetDate(docsBySifra[sifra][0])
            mostRecentDoc = docsBySifra[sifra][0]
            for doc in docsBySifra[sifra]:
                if GetDate(doc) > maxDate:
                    maxDate = GetDate(doc)
                    mostRecentDoc = doc
            documents.append(mostRecentDoc)
        else:
            documents.append(docsBySifra[sifra][0])    
    return documents

def FilterWrongType(doclist):
    docs = []
    for item in doclist:
        assert isinstance(item,Document)
        if item.CountNONE() < 6:
            docs.append(item)
    return docs

def countAtributes(documents,ignore = False):
    attrDict = {}
    for document in documents:
        assert isinstance(document,DocumentHTML)
        for row in document.FormatedRows:
            attribute = row[0]
            if ignore:
                if not any(bool(re.search(x,attribute)) for x in markers.TO_IGNORE):
                    if attribute not in attrDict:
                        attrDict[attribute] = 1
                    else:
                        attrDict[attribute] = attrDict[attribute] +1
            else:
                if attribute not in attrDict:
                    attrDict[attribute] = 1
                else:
                    attrDict[attribute] = attrDict[attribute] +1
                
    return attrDict

def removeEnglish(documents):
    """Remowes english documents based on whether the documnet date is defined"""
    return [x for x in documents if x.DatumIzdaje]