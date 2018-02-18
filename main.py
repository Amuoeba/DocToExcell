# -*- coding: utf-8 -*-
import parseXML as parser
import os
import testTools as tt
import createExcel
import tools

documents = []
excels = []

for file in os.listdir("./DocData/"):
    if file.endswith(".html"):        
        path = os.path.join("./DocData", file)
        doc = parser.Document(path,"table")
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
tt.testAll(documents)
#documents = tools.FilterWrongType(documents)
#documents = tools.FindMostRecent(documents)


#writer = createExcel.writeExcell(None)
#for ele in documents:
#    writer.createDocDataframe(ele)
#print (writer.dataframe)
#writer.write("test.xlsx")

wt = createExcel.ExcellWriter(documents)
#print(wt.DF)
wt.write("test1.xlsx")

