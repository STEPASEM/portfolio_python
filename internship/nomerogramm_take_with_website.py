from bs4 import BeautifulSoup
import asyncio
import requests
import json

"""
this program parses data from the Autoteca website.
"""

class poisk:
    def __init__(self, nomer):
        self.text_oh = 'По данному номеру ничего не найдено'
        self.url_refresh = 'http://api.autoteka.ru/user/refresh-session'
        self.url_nomer = f'http://api.autoteka.ru/preview/{nomer}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    async def prov_status(self):
        nomer_page = self.session.get(self.url_nomer)
        soup = BeautifulSoup(nomer_page.text, "html.parser")
        soup = json.loads(str(soup))
        return soup

    async def osn(self):
        self.session.get(self.url_refresh)
        soup = await self.prov_status()
        if 'status' in soup:
            while soup['status'] == 'wait':
                await asyncio.sleep(1)
                soup = await self.prov_status()
                if 'status' not in soup:
                    self.session.close()
                    return self.text_oh
            data = soup['data']
            self.session.close()
            print(data)
            return data
        else:
            self.session.close()
            return self.text_oh