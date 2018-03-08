# -*- coding: utf-8 -*-
import re
TO_IGNORE = set([re.compile("Izdelal:",re.IGNORECASE), re.compile("Mark:",re.IGNORECASE),
                 re.compile("Oznake:",re.IGNORECASE),re.compile("PDV|Priporočeni dnevni vnos"),re.compile("[*]Hranilna vrednost temelji na analizi\.",re.IGNORECASE),
                 re.compile("Pripravil:",re.IGNORECASE),re.compile("\/",re.IGNORECASE),re.compile(".*(?=hranilna).*(?=vrednost).*(?=temelji).*",re.IGNORECASE)])


SECTION_MARKERS = {"Opis":re.compile("opis izdelka",re.IGNORECASE),"Osnovne lastnosti":re.compile("osnovne lastnosti",re.IGNORECASE),
                   "Fizikalno kemijske zahteve":re.compile("fizikalno(?:.*?)kemijske",re.IGNORECASE),
                   "Sestavine":re.compile("sestavine",re.IGNORECASE),"Pakiranje":re.compile("PAKIRANJE"),"Zakonodaja":re.compile("zakonodaja",re.IGNORECASE),
                   "Aktivne učinkovine":re.compile("vsebnost|tabela|komponente",re.IGNORECASE)
                   }

JOIN_MARKERS = {"10 HDA":re.compile("10-* *HDA"),"Dimenzije KP":re.compile("Dimenzije KP",re.IGNORECASE),"Aktivne komponente":re.compile("aktivn|tabela|vsebnost",re.IGNORECASE),
                "Maščobe":re.compile("maščobe",re.IGNORECASE),"Ogljikovi hidrati":re.compile("ogljikovi hidrati",re.IGNORECASE),
                "Zakonodaja":re.compile("zakon",re.IGNORECASE),"Dimenzije MPE":re.compile("dimenzije mpe",re.IGNORECASE),
                "Fizikalno kemijske zahteve":re.compile("fizikaln",re.IGNORECASE),"Mikrobiološke zahteve":re.compile("mikrobio|mirobio",re.IGNORECASE),
                "Hranilna vrednost":re.compile("hranilna",re.IGNORECASE),"Kontrola":re.compile("izdelek je kontroliran",re.IGNORECASE)}