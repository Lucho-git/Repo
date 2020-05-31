from pathlib import Path
import requests


class Scraper:
    def __init__(self, path):
        self.path = path

    def download(self, url):
        filename = Path(self.path)
        response = requests.get(url)
        filename.write_bytes(response.content)
