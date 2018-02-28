# -*- coding: utf-8 -*-
import parseXML as parser
from parseXML import Document
from prepareUnstrructured import DocumentUnstructured
import os
import testTools as tt
import createExcel
import tools

documents = []
excels = []

for file in os.listdir("./DocData/"):
    if file.endswith(".html"):        
        path = os.path.join("./DocData", file)
        doc = parser.Document(path)
        if doc.CountNONE() > 6:
            doc = DocumentUnstructured(path)
        documents.append(doc)

#for i in documents:    
#    assert isinstance(i,parser.Document)
#    print("###############")
#    print(i.doc_name)
#    
#    for j in i.textByRow1:
#        print(j)
    
#tt.testAttrPressence(documents,'SENZORIČNE ')
#tt.testAttrFound(documents)
#tt.testSections(documents)
#tt.testHranilnaVrednost(documents)
#tt.testMikrobiloskeZahteve(documents)
#tt.testFizikalnoKemijskeZahteve(documents)
#tt.testPakiranje(documents)
#tt.testZakonodaja(documents)
#tt.testSingleSections(documents,"aktivne_učinkovine")
#tt.testAll(documents)
#documents = tools.FilterWrongType(documents)
documents = tools.FindMostRecent(documents)


#writer = createExcel.writeExcell(None)
#for ele in documents:
#    writer.createDocDataframe(ele)
#print (writer.dataframe)
#writer.write("test.xlsx")

wt = createExcel.ExcellWriter(documents)
#print(wt.DF)
wt.write("test1.xlsx","unstructTest.xlsx")
#t = None
#for i in documents:
#    if i.DocType == "2: Only textual":
#        t = i
#tt.test2(t)

