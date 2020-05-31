from classes.linkextraction import Extraction
from classes.pdfscraper import Scraper
from classes.pdf2text import PDF2text
from classes.cells import Cell

e = Extraction()
args = e.get_agmnts()
lnks = e.get_links()

print(args)
print(lnks)

cells = list()

p = Scraper('pdfs/')
conv = PDF2text('pdfs/text/')
count = 0
for url in lnks:
    arg = args[count]
    p.download(url, arg)
    conv.run('pdfs/' + arg + '.pdf', arg)
    addCell = Cell(arg, url, 'pdfs/'+arg+'.pdf', 'pdfs/text/'+arg+'.txt')
    cells.append(addCell)

    count += 1

cells[0].gather_text()
cells[0].return_search('gay')

searchterms = ["AustralianSuper", "Australian Super", "Westscheme", "Australian Superannuation Scheme"]


