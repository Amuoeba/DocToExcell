# -*- coding: utf-8 -*-
import re

TO_IGNORE = set([re.compile("Izdelal:",re.IGNORECASE), re.compile("Mark:",re.IGNORECASE),
                 re.compile("Oznake:",re.IGNORECASE),re.compile("PDV|Priporočeni dnevni vnos"),re.compile("[*]Hranilna vrednost temelji na analizi\.",re.IGNORECASE),
                 re.compile("Pripravil:",re.IGNORECASE),re.compile("\/",re.IGNORECASE),re.compile(".*(?=hranilna).*(?=vrednost).*(?=temelji).*",re.IGNORECASE)])


SECTION_MARKERS = {"Opis":re.compile("opis izdelka",re.IGNORECASE),"Osnovne lastnosti":re.compile("osnovne lastnosti",re.IGNORECASE),
                   "Fizikalno kemijske zahteve":re.compile("fizikalno(?:.*?)kemijske",re.IGNORECASE),
                   "Sestavine":re.compile("sestavine",re.IGNORECASE),"Pakiranje":re.compile("PAKIRANJE"),"Zakonodaja":re.compile("zakonodaja",re.IGNORECASE),
                   "Aktivne učinkovine":re.compile("vsebnost|tabela|komponente|aktivnih|vitamini",re.IGNORECASE,),"Hranilna vrednost":re.compile("hranilna",re.IGNORECASE),
                   "Mikrobiološke zahteve":re.compile("mikrobio|mirobio",re.IGNORECASE),"Senzorične zahteve":re.compile("senzorične zahteve",re.IGNORECASE)}

JOIN_MARKERS = {"10 HDA":re.compile("10-* *HDA"),"Dimenzije KP":re.compile("Dimenzije KP",re.IGNORECASE),"Aktivne komponente":re.compile("aktivn|tabela|vsebnost",re.IGNORECASE),
                "Maščobe":re.compile("maščobe",re.IGNORECASE),"Ogljikovi hidrati":re.compile("ogljikovi hidrati",re.IGNORECASE),
                "Zakonodaja":re.compile("zakon",re.IGNORECASE),"Dimenzije MPE":re.compile("dimenzije mpe",re.IGNORECASE),
                "Fizikalno kemijske zahteve":re.compile("fizikaln",re.IGNORECASE),"Mikrobiološke zahteve":re.compile("mikrobio|mirobio",re.IGNORECASE),
                "Hranilna vrednost":re.compile("hranilna",re.IGNORECASE),"Kontrola":re.compile("izdelek je kontroliran",re.IGNORECASE),
                "Tip KP":re.compile("Tip.*(?=komerci).*",re.IGNORECASE),"Tip MPE":re.compile("Tip.*(?=maloprod).*",re.IGNORECASE)}

EXTRACTION_MARKERS = {"Opis izdelka":re.compile("opis izdelka",re.IGNORECASE),"Sestavine":re.compile("sestavine",re.IGNORECASE),
                      "Senzorične zahteve":re.compile("senzorične zahteve",re.IGNORECASE),"Mikrobiološke zahteve":re.compile("mikrobiološke|mirobio",re.IGNORECASE),
                      "Fizikalno kemijske zahteve":re.compile("fizikaln",re.IGNORECASE),"Aktivne učinkovine":re.compile("vsebnost|tabela|komponente|aktivnih|vitamini"),
                      "Hranilna vrednost":re.compile("hranilna",re.IGNORECASE)}



UNITS = re.compile("(?<=[0-9] |.[0-9])([a-ž%µ]{1,3}(?: *\/ *[a-z%µ]{1,3})*|kcal)(?![a-z])",re.IGNORECASE)
MAX = re.compile("(?:< *|≤ *|max\. *)+([0-9]+(?:[,.]*[0-9]*))|(?:(?:-|—|–) *)([0-9]+(?:[,.]*[0-9]*))",re.IGNORECASE)
MIN = re.compile("(?:> *|≥ *|min\. *)+([0-9]+(?:[,.]*[0-9]*))|([0-9]+(?:[,.]*[0-9]*))(?: *(?:-|—|–))",re.IGNORECASE)


MICROBIOLOGICAL = {"Value":re.compile("^(?:≤*|<*|max\.) *(neg.|[0-9]+(?:,|\.)*[0-9]*)",re.IGNORECASE),"Unit":re.compile("(?:[A-Za-z]{3})* *(?:\/ *)(?:[0-9]*(?:,|\.)*[0-9]* *[A-Za-z]*)",re.IGNORECASE)}
FIZKEM = {"Value":re.compile("([0-9]+(?:,|\.)*[0-9]*)",re.IGNORECASE),"Vodilni cvetni prahovi":re.compile("vodilni cvetni prah")}
HRANILNA = {"Na":re.compile("^na | na |^per | per ",re.IGNORECASE),"Per":re.compile("[0-9]+[,.]*[0-9]* *(?:[a-ž%µ]{1,3}(?: *\/ *[a-z%µ]{1,3})*|kcal)(?![a-ž])",re.IGNORECASE)}







# String formatting markers

REPLACERS = {"neg.":re.compile("neg\.",re.IGNORECASE)}