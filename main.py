# -*- coding: utf-8 -*-
import parseXML as parser
import os

documents = []

for file in os.listdir("./DocData/"):
    if file.endswith(".xml"):        
        path = os.path.join("./DocData", file)
        doc = parser.Document(path,"table")
        documents.append(doc)

for i in documents:    
    assert isinstance(i,parser.Document)
    print("###############")
    print(i.doc_name)
    i.preety_print()