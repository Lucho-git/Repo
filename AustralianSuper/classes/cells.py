import io
import re
from classes.agreement import Agreement
from classes.spreadsheet import Spread


class Cell:
    def __init__(self, argument, link, pdfpath, textpath, agreement, spread):
        self.argument = argument
        self.link = link
        self.pdfpath = pdfpath
        self.textpath = textpath
        self.text = ""
        self.contains = ""
        self.agreement = agreement
        self.spread = spread

    def add_agreement(self, in_ag):
        self.agreement = in_ag

    def gather_text(self):
        f = open(self.textpath)
        self.text = f.read()

    def return_search(self, searchterms):
        caps = self.text.upper()
        retstring = ""
        for st in searchterms:
            count = caps.count(st)
            '''print(st + ":" + str(count))'''
            if count > 0:
                retstring += st + "."+str(count)+" "
        if not retstring == "":
            self.contains = retstring
        return retstring


    def return_first_term(self, searchterms):
        caps = self.text.upper()
        min_val = 9999999
        first_term = None
        for st in searchterms:
            size = caps.find(st)
            if size < min_val:
                min_val = size
                first_term = st
        if min_val < 9999999:
            return first_term
        else:
            print("NO SEARCH TERMS MATCHED")

