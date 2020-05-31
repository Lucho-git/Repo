class Cell:
    def __init__(self, argument, link, pdfpath, textpath):
        self.argument = argument
        self.link = link
        self.pdfpath = pdfpath
        self.textpath = textpath
        self.text = ""



    def gather_text(self):
        f = open(self.textpath)
        self.text = f.read()

    def return_search(self, searchterms):
        print(self.text)
