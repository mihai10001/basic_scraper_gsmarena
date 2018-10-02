import urllib.request
from bs4 import BeautifulSoup
from pymongo import MongoClient


def scrape_info():
    results = []
    pages = []

    for page in pages:
        item = {}
        webpage = urllib.request.urlopen(page)
        soup = BeautifulSoup(webpage, 'html.parser')
        name_box = soup.find('h1', attrs={'class': 'specs-phone-name-title'})
        date_box = soup.find('td', attrs={'class': 'nfo', 'data-spec': 'year'})
        proc_box = soup.find('div', attrs={'data-spec': 'chipset-hl'})
        price_box = soup.find('td', attrs={'class': 'nfo', 'data-spec': 'price'})

        name = name_box.text.strip()
        date = date_box.text.strip()

        if price_box:
            price = price_box.text.strip()
            item["price"] = price.split()[1] + ' $'
        else:
            item["price"] = '-'

        item["rating"] = '-'
        item["model"] = name
        item["brand"] = name.split()[0]
        item["date"] = ' '.join(date.split(', '))
        item["proc"] = proc_box.text.strip()
        results.append(item)

    return results


client = MongoClient('localhost', 27017)
db = client['local']
collection = db['phone']
res = scrape_info()
collection.insert_many(res)
