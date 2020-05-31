import io
import re


class Info:
    def __init__(self):
        self.info = ''

    def gather(self, cell):
        f = open(cell.textpath)
        contents = f.read()
        return contents

    def does_contain(self, searchterms):
