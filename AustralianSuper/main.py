from classes.linkextraction import Extraction
from classes.pdfscraper import Scraper


e = Extraction()
print(e.get_agmnts())
print(e.get_links())

p = Scraper('pdfs/metadata.pdf')
p.download(e.get_links()[0])


