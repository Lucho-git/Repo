from pathlib import Path
import requests

filename = Path('pdfs/metadata.pdf')
url = 'https://www.fwc.gov.au/documents/documents/agreements/fwa/ae507950.pdf'
response = requests.get(url)
filename.write_bytes(response.content)
