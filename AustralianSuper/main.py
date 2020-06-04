from classes.linkextraction import Extraction
from classes.pdfscraper import Scraper
from classes.pdf2text import PDF2text
from classes.cells import Cell
from classes.spreadsheet import Spread
from classes.agreement import Agreement

import os.path

e = Extraction()

'''Gets the arguments list from a text file'''
args = e.get_agmnts()
'''Creates the pdf links using the arguments from the fairwork.gov.au website'''
lnks = e.get_links()
'''Gets the full excel spreet agreements'''
agreements = e.get_agreements()
print(args)
print(lnks)
print(len(agreements))

cells = list()

'''initialize webscraper'''
p = Scraper('pdfs/')

'''initialize text converter'''
conv = PDF2text('pdfs/text/')


count = 0
for url in lnks:
    arg = agreements[count].agmnt
    if not os.path.isfile("pdfs/"+arg+".pdf"):
        '''downloads the pdfs using the argument generated links'''
        print("Downloading new pdf file: "+arg)
        p.download(url, arg)

    if not os.path.isfile("pdfs/text/"+arg+".txt"):
        '''Converts PDF Documents into text, note a significant portion of these documents contain scanned 
        in information, or non text metadata that is impossible for it to convert'''
        print("Making new text file: "+arg)
        conv.run('pdfs/' + arg + '.pdf', arg)

    addSpread = Spread()
    addCell = Cell(arg, url, 'pdfs/'+arg+'.pdf', 'pdfs/text/'+arg+'.txt', agreements[count], addSpread)
    addCell.spread.set_agreement_values(addCell.link, addCell.argument, addCell.agreement.title, addCell.agreement.print_n,
                                        addCell.agreement.industry, addCell.agreement.operative, addCell.agreement.expiry)
    cells.append(addCell)
    count += 1



searchterms = ["AUSTRALIANSUPER", "AUSTRALIAN SUPER", "WESTSCHEME", "AUSTRALIAN SUPERANNUATION SCHEME"]

tcount = 0
fcount = 0
nfcount = 0
term_list = list()

for i in cells:
    i.gather_text()
    results = i.return_search(searchterms)
    tcount += 1
    if results:
        fcount += 1
        term_list.append(i)
    else:
        nfcount += 1

industry_list = list()
for t in term_list:
    found = False
    for i in industry_list:
        if t.agreement.industry == i:
            found = True
    if not found:
        industry_list.append(t.agreement.industry)

for i in industry_list:
    in_count = 0
    for t in term_list:
        if t.agreement.industry == i:
            in_count += 1
    i += "," + str(in_count)
    '''print(i)'''




for i in cells:
    if not i.contains == "":
        pass

searchcities = ["SYDNEY", "MELBOURNE", "BRISBANE", "PERTH", "ADELAIDE", "GOLD COAST",
                "NEWCASTLE", "CANBERRA", "SUNSHINE COAST", "WOLLONGONG", "GEELONG", "HOBART",
                "TOWNSVILLE", "CAIRNS", "DARWIN", "TOOWOOMBA", "BALLARAT", "BENDIGO", "ALBURY",
                "LAUNCESTON", "MACKAY", "ROCKHAMPTON", "BUNBURY", "COFFS HARBOUR", "BUNDABERG",
                "WAGGA WAGGA", "HERVEY BAY", "BUSSELTON", "GERALDTON"]

for i in cells:
    i.gather_text()
    results = i.return_first_term(searchcities)
    if results:
        i.spread.set_approval(results)



print(cells[0].spread.make_list())
print(cells[1].spread.make_list())
print(cells[2].spread.make_list())
print(cells[3].spread.make_list())
spreadstring = ""
for c in cells:
    spreadstring += c.spread.format_spread()

f = open("output/out.txt", "w+")
f.write(spreadstring)