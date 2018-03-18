# -*- coding: utf-8 -*-
import re

def cleanPer(perList):
    """ Removes elements of "per" list if two elements have too similar value"""
    valueRe = re.compile("([0-9]+(?:,|\.)*[0-9]*)",re.IGNORECASE)
    perValues = []
    for ele in perList:
        val = re.findall(valueRe,ele)
        if val != []:
            perValues = perValues + val
    perValues = [float(x.replace(",",".")) for x in perValues]
    
    toRemove = []
    for x in enumerate(perValues):
        for y in enumerate(perValues[x[0]:]):
            val_x = x[1]
            val_y = y[1]
            quotient = val_x/val_y
            if (quotient > 0.75 and quotient < 1.0) or (quotient < 1.35 and quotient > 1.0):
                toRemove.append(y[0])
    toRemove.sort(reverse=True)
    for i in toRemove:
        perList.pop(i)
    return perList
