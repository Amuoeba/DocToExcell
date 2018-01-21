# -*- coding: utf-8 -*-
import parseXML as parser
import os
import testTools as tt

documents = []
excels = []

for file in os.listdir("./DocData/"):
    if file.endswith(".html"):        
        path = os.path.join("./DocData", file)
        doc = parser.Document(path,"table")
        documents.append(doc)

for i in documents:    
    assert isinstance(i,parser.Document)
    print("###############")
    print(i.doc_name)
    
    for j in i.textByRow1:
        print(j)
    
tt.testAttrPressence(documents,'SENZORIČNE ')
tt.testAttrFound(documents)

