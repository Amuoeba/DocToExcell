# -*- coding: utf-8 -*-
import re
TO_IGNORE = set([re.compile("Izdelal:",re.IGNORECASE), re.compile("Mark:",re.IGNORECASE),
                 re.compile("Oznake:",re.IGNORECASE),re.compile("PDV"),re.compile("[*]Hranilna vrednost temelji na analizi\.",re.IGNORECASE)])


SECTION_MARKERS = {"Opis":re.compile("opis izdelka",re.IGNORECASE),"Osnovne lastnosti":re.compile("osnovne lastnosti",re.IGNORECASE),
                   "Fizikalno kemijske zahteve":re.compile("fizikalno(?:.*?)kemijske",re.IGNORECASE),
                   "Sestavine":re.compile("sestavine",re.IGNORECASE),"Pakiranje":re.compile("PAKIRANJE"),"Zakonodaja":re.compile("zakonodaja",re.IGNORECASE)
                   }