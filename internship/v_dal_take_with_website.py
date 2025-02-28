from bs4 import BeautifulSoup
import requests

"""
a parser from Dahl's website
"""

class poisk:

    def __init__(self, bukv):
        self.session = requests.Session()
        self.url = f'https://v-dal.ru/?f={bukv}&action=q'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        self.session.headers.update(self.headers)

    async def osn(self):
        vivod = []
        page = self.session.get(self.url)
        page.encoding = page.apparent_encoding
        soup = BeautifulSoup(page.text, "html.parser")
        for div in soup.find_all('div', style="padding: 20 20 0 10; text-align:justify"):
            vivod = div.get_text().split("\n")[4][1:].split("  ")
        self.session.close()
        if vivod == ['']:
            return 'Такого слова нет в словаре Даля'
        return vivod
