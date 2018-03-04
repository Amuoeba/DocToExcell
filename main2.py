# -*- coding: utf-8 -*-
import parseHTML as parser
from parseHTML import DocumentHTML
from prepareUnstrructured import DocumentUnstructured
import os
import testTools as tt
import createExcel
import tools
import re

documents = []
excels = []

for file in os.listdir("./RealDataHTML"):
    SPre = re.compile("^SP")
    ANGre = re.compile("ANG")
#    print(bool(re.match(SPre,file)),bool(re.findall(ANGre,file)))
    
    if file.endswith(".html") and bool(re.match(SPre,file)) and not bool(re.findall(ANGre,file)):        
        print(file)
        path = os.path.join("./RealDataHTML", file)
        doc = parser.DocumentHTML(path)
        documents.append(doc)
print(len(documents))
documents = tools.FindMostRecent(documents)
print(len(documents))
attributes = tools.countAtributes(documents)