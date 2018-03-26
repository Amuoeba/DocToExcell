# -*- coding: utf-8 -*-
import re

TO_IGNORE = set([re.compile("Izdelal:",re.IGNORECASE), re.compile("Mark:",re.IGNORECASE),
                 re.compile("Oznake:",re.IGNORECASE),re.compile("PDV|Priporočeni dnevni vnos"),re.compile("[*]Hranilna vrednost temelji na analizi\.",re.IGNORECASE),
                 re.compile("Pripravil:",re.IGNORECASE),re.compile("\/",re.IGNORECASE),re.compile(".*(?=hranilna).*(?=vrednost).*(?=temelji).*",re.IGNORECASE)])


SECTION_MARKERS = {"Opis":re.compile("opis izdelka",re.IGNORECASE),"Osnovne lastnosti":re.compile("osnovne lastnosti",re.IGNORECASE),
                   "Fizikalno kemijske zahteve":re.compile("fizikaln[oe](?:.*?)kemijske",re.IGNORECASE),
                   "Sestavine":re.compile("sestavine",re.IGNORECASE),"Pakiranje":re.compile("PAKIRANJE"),"Zakonodaja":re.compile("zakonodaja",re.IGNORECASE),
                   "Aktivne učinkovine":re.compile("vsebnost|tabela|komponente|aktivnih|vitamini",re.IGNORECASE,),"Hranilna vrednost":re.compile("hranilna",re.IGNORECASE),
                   "Mikrobiološke zahteve":re.compile("mikrobio|mirobio",re.IGNORECASE),"Senzorične zahteve":re.compile("senzorične zahteve",re.IGNORECASE)}

JOIN_MARKERS = {'10 HDA': re.compile(r'10-* *HDA', re.UNICODE),
 'Aerobne mezofilne bakterije': re.compile(r'aerobn[ei] mezofiln[ei]',
 re.IGNORECASE|re.UNICODE),
 'Bacilus cereus': re.compile(r'bacillu[s]* cereus', re.IGNORECASE|re.UNICODE),
 'Dimenzije KP': re.compile(r'Dimenzije KP', re.IGNORECASE|re.UNICODE),
 'Dimenzije MPE': re.compile(r'dimenzije mpe', re.IGNORECASE|re.UNICODE),
 'Escherichia coli': re.compile(r'e\. coli|e[sc]*herichia col',
 re.IGNORECASE|re.UNICODE),
 'Fizikalno kemijske zahteve': re.compile(r'fizikaln',
 re.IGNORECASE|re.UNICODE),
 'Hranilna vrednost': re.compile(r'hranilna', re.IGNORECASE|re.UNICODE),
 'Koagulaza pozitivni stafilokoki in Staphylococcus aureus': re.compile(r'koagul[a]*za pozitivni',
 re.IGNORECASE|re.UNICODE),
 'Kontrola': re.compile(r'izdelek je kontroliran', re.IGNORECASE|re.UNICODE),
 'Maščobe': re.compile(r'maščobe', re.IGNORECASE|re.UNICODE),
 'Mikrobiološke zahteve': re.compile(r'mikrobio|mirobio',
 re.IGNORECASE|re.UNICODE),
 'Natrij': re.compile(r'natrij', re.IGNORECASE|re.UNICODE),
 'Niacin': re.compile(r'niacin', re.IGNORECASE|re.UNICODE),
 'Ogljikovi hidrati': re.compile(r'ogljikovi hidrati',
 re.IGNORECASE|re.UNICODE),
 'Okus in aroma': re.compile(r'aroma in okus|okus in aroma', re.IGNORECASE|re.UNICODE),
 'Vonj':re.compile('vonj|aroma',re.IGNORECASE|re.UNICODE),
 'Salmonella': re.compile(r'salmonella', re.IGNORECASE|re.UNICODE),
 'Skupno št. mikroorganizmov': re.compile(r'skupn[oie]',
 re.IGNORECASE|re.UNICODE),
 'Staphylococcus aureus': re.compile(r'^staph[y]*lococcus aureus',
 re.IGNORECASE|re.UNICODE),
 'Sulfit reducirajoči klostridij': re.compile(r'sulfit|sulphite',
 re.IGNORECASE|re.UNICODE),
 'Tip KP': re.compile(r'Tip.*(?=komerci).*', re.IGNORECASE|re.UNICODE),
 'Tip MPE': re.compile(r'Tip.*(?=maloprod).*', re.IGNORECASE|re.UNICODE),
 'Vlaga': re.compile(r'vlag[ae]', re.IGNORECASE|re.UNICODE),
 'Zakonodaja': re.compile(r'zakon', re.IGNORECASE|re.UNICODE),
 'Sol': re.compile(r'sol', re.IGNORECASE|re.UNICODE)}

EXTRACTION_MARKERS = {"Opis izdelka":re.compile("opis izdelka",re.IGNORECASE),"Sestavine":re.compile("sestavine",re.IGNORECASE),
                      "Senzorične zahteve":re.compile("senzorične zahteve",re.IGNORECASE),"Mikrobiološke zahteve":re.compile("mikrobiološke|mirobio",re.IGNORECASE),
                      "Fizikalno kemijske zahteve":re.compile("fizikaln",re.IGNORECASE),"Aktivne učinkovine":re.compile("vsebnost|tabela|komponente|aktivnih|vitamini|učinkovine",re.IGNORECASE),
                      "Hranilna vrednost":re.compile("hranilna",re.IGNORECASE),"Pakiranje":re.compile("PAKIRANJE",re.IGNORECASE),"Zakonodaja":re.compile("zakonodaja",re.IGNORECASE)}



UNITS = re.compile("(?<=[0-9] |.[0-9])([a-ž%µ]{1,3}(?: *\/ *[a-z%µ]{1,3})*|kcal)(?![a-z])",re.IGNORECASE)
MAX = re.compile("(?:< *|≤ *|max\. *)+([0-9]+(?:[,.]*[0-9]*))|(?:(?:-|—|–) *)([0-9]+(?:[,.]*[0-9]*))",re.IGNORECASE)
MIN = re.compile("(?:> *|≥ *|min\. *)+([0-9]+(?:[,.]*[0-9]*))|([0-9]+(?:[,.]*[0-9]*))(?: *(?:-|—|–))",re.IGNORECASE)


MICROBIOLOGICAL = {"Value":re.compile("^(?:≤*|<*|max\.) *(neg\.*|[0-9]+(?:,|\.)*[0-9]*)",re.IGNORECASE),"Unit":re.compile("(?:[cfu]{3})* *(?:\/ *)(?:[0-9]*(?:,|\.)*[0-9]* *[A-Za-z]*)",re.IGNORECASE)}
FIZKEM = {"Value":re.compile("([0-9]+(?:,|\.)*[0-9]*)",re.IGNORECASE),"Vodilni cvetni prahovi":re.compile("vodilni cvetni prah")}
HRANILNA = {"Na":re.compile("^na | na |^per | per ",re.IGNORECASE),"Per":re.compile("[0-9]+[,.]*[0-9]* *(?:[a-ž%µ]{1,3}(?: *\/ *[a-z%µ]{1,3})*|kcal)(?![a-ž])",re.IGNORECASE)}
AKTIVNE = {"Na":re.compile("^na | na |^per | per | steklenič| kapsul",re.IGNORECASE),"Per":re.compile("[0-9]+[,.]*[0-9]* *(?:[a-ž%µ]{1,3}(?: *\/ *[a-z%µ]{1,3})*|kcal)(?![a-ž])",re.IGNORECASE)}
PAKIRANJE = {"neto":re.compile("neto koli[a-ž]*?",re.IGNORECASE),
#                   "embalaža":re.compile("embalaža",re.IGNORECASE),
                   "tip MPE":re.compile("tip mpe",re.IGNORECASE),
                   "tip TP":re.compile("tip tp",re.IGNORECASE),
                   "tip KP":re.compile("tip kp",re.IGNORECASE),
                   "dimenzija MPE":re.compile("dime[a-ž]*? mpe",re.IGNORECASE),
                   "dimenzija TP":re.compile("dime[a-ž]*? tp",re.IGNORECASE),
                   "dimenzija KP":re.compile("dime[a-ž]*? kp",re.IGNORECASE),
                   "število MPE":re.compile("število mpe na",re.IGNORECASE),
                   "število plasti na paleti":re.compile("število plasti na pale",re.IGNORECASE),
                   "način transporta":re.compile("način transporta",re.IGNORECASE),
                   "način skladiščenja":re.compile("način skladiščenja",re.IGNORECASE),
                   "rok uporabe":re.compile("rok upo",re.IGNORECASE)}





# String formatting markers

REPLACERS = {"neg.":re.compile("neg",re.IGNORECASE)}