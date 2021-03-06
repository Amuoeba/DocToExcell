import parseXML
from prepareUnstrructured import DocumentUnstructured
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
#        netoKolicina = doc.NetoKolicina
        videz = doc.Izgled
        aroma = doc.Vonj
        zakonodaja = doc.Zakonodaja
        print("###### DOCNAME: ",doc.doc_name)
        print("Naziv: ",colored(naziv,chooseColor(naziv)))
        print("Sifra: ",colored(sifra,chooseColor(sifra)))
        print("Opis Izdelka: ",colored(opisIzdelka,chooseColor(opisIzdelka)))
        print("Sestavine: ",colored(sestavine,chooseColor(sestavine)))
#        print("Neto Količina: ",colored(netoKolicina,chooseColor(netoKolicina)))
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

def testSingleSections(doclist,section):
    for document in doclist:
        assert isinstance(document,parseXML.Document)
        if section in document.Sections:
            print("######### ", document.doc_name)    
            print("---------------------%%%%%%%%%%%%%%%%%%")
            print("Section: ", colored(section,"green"), "\n" )
            print(document.Sections[section])
            print("---------------------%%%%%%%%%%%%%%%%%%")
        else:
            print("######### ", document.doc_name)
            print("---------------------%%%%%%%%%%%%%%%%%%")
            print(colored(section + " not present " ,"red"))
            print("---------------------%%%%%%%%%%%%%%%%%%")

def testHranilnaVrednost(doclist):
    for document in doclist:
        assert isinstance(document,parseXML.Document)

        if document.HranilnaVrednost:
            print("######### ", document.doc_name)
            print("---------------------")
            for v in document.HranilnaVrednost:                
                print(colored(v,"green"),": ",document.HranilnaVrednost[v])
            print("---------------------")
                    
        else:
            print("######### ", document.doc_name)
            print("---------------------")
            print(colored("Hranilna vrednost" + " not present ","red"))
            print("---------------------")
            
def testMikrobiloskeZahteve(doclist):
    for document in doclist:
        assert isinstance(document,parseXML.Document)
        if document.MikrobiloskeZahteve:
            print("######### ", document.doc_name)
            print("---------------------")
            for i in document.MikrobiloskeZahteve:
                print(colored(i,"green"),": ",document.MikrobiloskeZahteve[i])
            print("---------------------")
        else:
            print("######### ", document.doc_name)
            print("---------------------")
            print(colored("Mikrobiloške zahteve" + " not present ","red"))
            print("---------------------")
            
def testFizikalnoKemijskeZahteve(doclist):
    for document in doclist:
        assert isinstance(document,parseXML.Document)
        if document.FizikalnoKemijskeZahteve:
            print("######### ", document.doc_name)
            print("---------------------")
            for i in document.FizikalnoKemijskeZahteve:
                print(colored(i,"green"),": ",document.FizikalnoKemijskeZahteve[i])
            print("---------------------")
        else:
            print("######### ", document.doc_name)
            print("---------------------")
            print(colored("Fizikalno kemijske zahteve" + " not present ","red"))
            print("---------------------")

def testPakiranje(doclist):
    for document in doclist:
        assert isinstance(document, parseXML.Document)
        if document.Pakiranje:
            print("######### ", document.doc_name)
            print("---------------------")
            for i in document.Pakiranje:                
                print(colored(i,"green"),": ",document.Pakiranje[i])
            print("---------------------")
        else:
            print("######### ", document.doc_name)
            print("---------------------")
            print(colored("Pakiranje" + " not present ","red"))
            print("---------------------")

def testZakonodaja(doclist):
    for document in doclist:
        if document.Zakonodaja:
            print("######### ", document.doc_name)
            print("---------------------")
            print(colored("Zakonodaja","green"),": ",document.Zakonodaja)
            print("---------------------")
        else:
            print("######### ", document.doc_name)
            print("---------------------")
            print(colored("Zakonodaja" + " not present ","red"))
            print("---------------------")
    
def testAll(doclist):
    def chooseColor(value):
        if value:
            return "green"
        else:
            return "red"
    
    for document in doclist:        
        assert isinstance(document,parseXML.Document)
        naziv = document.Naziv
        sifra = document.Sifra
        hranilna = document.HranilnaVrednost
        mikrobioloske = document.MikrobiloskeZahteve
        fizkem = document.FizikalnoKemijskeZahteve
        pakiranje = document.Pakiranje
        zakonodaja = document.Zakonodaja
        sestavine = document.Sestavine
        opis = document.OpisIzdelka
        aroma = document.Vonj
        videz = document.Izgled
        aktivneU = document.AktivneUcinkovine
        print("###### DOCNAME: ",document.doc_name)
        print("Datum izdaje")
        print("Naziv: ",colored(naziv,chooseColor(naziv)))
        print("Sifra: ",colored(sifra,chooseColor(sifra)))
        print("Opis Izdelka: ",colored(opis,chooseColor(opis)))
        print("Sestavine: ",colored(sestavine,chooseColor(sestavine)))
#        print("Neto Količina: ",colored(netoKolicina,chooseColor(netoKolicina)))
        print("Videz: ",colored(videz,chooseColor(videz)))
        print("Aroma: ",colored(aroma,chooseColor(aroma)))
        print("Hranilna vrednost: ",colored(hranilna,chooseColor(hranilna)))
        print("Mikrobiloške zahteve: ",colored(mikrobioloske,chooseColor(mikrobioloske)))
        print("Fizikalno kemijske: ",colored(fizkem,chooseColor(fizkem)))
        print("Aktivne  ucinkovine: ", colored(aktivneU,chooseColor(aktivneU)))
        print("Pakiranje: ",colored(pakiranje,chooseColor(pakiranje)))
        print("Zakonodaja: ",colored(zakonodaja,chooseColor(zakonodaja)))
        
        
        
        
def test2(doc):
    assert isinstance(doc,DocumentUnstructured)
    print(doc.rows)
        