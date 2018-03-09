# -*- coding: utf-8 -*-

class Attribute():    
    def __init__(self,name,value):
        self.name = name
        self.value = value
    
    def nicePrint(self):
        return "Name: "+ self.name +"Value: " + self.value