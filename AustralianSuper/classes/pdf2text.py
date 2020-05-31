from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
import sys



class PDF2text:
    def __init__(self, path):
        self.path = path

    def run(self, filepath, arg):

        # debug option
        debug = 0
        # input option
        password = ''
        pagenos = set()
        maxpages = 0
        # output option
        outfile = self.path + arg + '.txt'
        outtype = 'text'
        imagewriter = None
        rotation = 0
        stripcontrol = False
        layoutmode = 'normal'
        codec = 'utf-8'
        pageno = 1
        scale = 1
        caching = True
        showpageno = True
        laparams = LAParams()

        #
        PDFDocument.debug = debug
        PDFParser.debug = debug
        CMapDB.debug = debug
        PDFPageInterpreter.debug = debug
        #
        rsrcmgr = PDFResourceManager(caching=caching)

        if outfile:
            outfp = open(outfile, 'w')
        else:
            outfp = sys.stdout
        if outtype == 'text':
            device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                                   imagewriter=imagewriter)
        elif outtype == 'xml':
            device = XMLConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                                  imagewriter=imagewriter,
                                  stripcontrol=stripcontrol)

        fp = open(filepath, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, pagenos,
                                      maxpages=maxpages, password=password,
                                      caching=caching, check_extractable=True):
            page.rotate = (page.rotate + rotation) % 360
            interpreter.process_page(page)
        fp.close()

        device.close()
        outfp.close()

        print("Converted PDF to Text")
        return
