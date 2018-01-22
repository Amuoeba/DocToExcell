import parseXML
from termcolor import colored


#print (colored('hello', 'red'), colored('world', 'green'))

def testAttrPressence(docList,attrList):
    if not isinstance(attrList,list):
        attrList = [attrList]
    
    for doc in docList:
        assert isinstance(doc,parseXML.Document)
        rows = doc.textByRow
        
        allRows = []
        for i in rows:
            allRows = allRows + i
        if set(attrList).issubset(allRows):
            print(colored(" True ","green")+doc.doc_name  )
        else:
            print(colored(" False ","red")+doc.doc_name  )
            
    return None

def testAttrFound(docList):
    def chooseColor(value):
        if value:
            return "green"
        else:
            return "red"
    
    for doc in docList:
        assert isinstance(doc, parseXML.Document)
        naziv = doc.Naziv
        sifra = doc.Sifra
        opisIzdelka = doc.OpisIzdelka
        sestavine = doc.Sestavine
        netoKolicina = doc.NetoKolicina
        videz = doc.Videz
        aroma = doc.Aroma
        zakonodaja = doc.Zakonodaja
        print("###### DOCNAME: ",doc.doc_name)
        print("Naziv: ",colored(naziv,chooseColor(naziv)))
        print("Sifra: ",colored(sifra,chooseColor(sifra)))
        print("Opis Izdelka: ",colored(opisIzdelka,chooseColor(opisIzdelka)))
        print("Sestavine: ",colored(sestavine,chooseColor(sestavine)))
        print("Neto Količina: ",colored(netoKolicina,chooseColor(netoKolicina)))
        print("Videz: ",colored(videz,chooseColor(videz)))
        print("Aroma: ",colored(aroma,chooseColor(aroma)))
        print("Zakonodaja: ",colored(zakonodaja,chooseColor(zakonodaja)))

def testSections(doclist):
    for document in doclist:
        assert isinstance(document,parseXML.Document)
        print("######### ", document.doc_name)
        for section in document.Sections:
            print("---------------------")
            print("Section: ", section, "\n" )
            print(document.Sections[section])
            print("---------------------")
            
        
        
                          
    