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

for file in os.listdir("./RealDataHTML2"):
    SPre = re.compile("^SP [0-9]{3,}")
    ANGre = re.compile("((?:ANG|ang) *[0-9]* *.html|ANG)")
#    print(bool(re.match(SPre,file)),bool(re.findall(ANGre,file)))
    
    if file.endswith(".html") and bool(re.search(SPre,file)) and not bool(re.search(ANGre,file)): #and bool(re.search(SPre,file))) and !bool(re.search(ANGre,file)):        
        print(file)
        path = os.path.join("./RealDataHTML2", file)
        doc = parser.DocumentHTML(path)
        documents.append(doc)
print(len(documents))
documents = tools.removeEnglish(documents)
documents = tools.FindMostRecent(documents)
print(len(documents))
attributes = tools.countAtributes(documents,ignore=True)