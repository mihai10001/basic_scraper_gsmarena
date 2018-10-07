import time
import urllib.request
from bs4 import BeautifulSoup
from pymongo import MongoClient


def scrape_brands():
    results = []
    brands_page = 'https://www.gsmarena.com/makers.php3'
    webpage = urllib.request.urlopen(brands_page)
    soup = BeautifulSoup(webpage, 'html.parser')

    for tr in soup.find_all('tr'):
        for td in tr.findChildren('td'):
            results.append('https://www.gsmarena.com/' + td.find('a')['href'])

    return results


# only scrapes the first page of results = maximum 40 phones from each brand
# sorted by release date
def scrape_devices_from_brand(brand_page):
    results = []

    webpage = urllib.request.urlopen(brand_page)
    soup = BeautifulSoup(webpage, 'html.parser')
    phones_box = soup.find('div', attrs={'class': 'makers'})
    ul = phones_box.find('ul')

    for li in ul.find_all('li'):
        results.append('https://www.gsmarena.com/' + li.find('a')['href'])

    return results


# ugly one liners for simplified view
def scrape_device_info(device_page):
    item = {}
    webpage = urllib.request.urlopen(device_page)
    soup = BeautifulSoup(webpage, 'html.parser')

    name_box = soup.find('h1', attrs={'class': 'specs-phone-name-title'})
    date_box = soup.find('td', attrs={'class': 'nfo', 'data-spec': 'year'})
    proc_box = soup.find('div', attrs={'data-spec': 'chipset-hl'})
    price_box = soup.find('td', attrs={'class': 'nfo', 'data-spec': 'price'})
    rating_box = soup.find('strong', attrs={'class': 'accent'})

    item["price"] = price_box.text.strip().split()[1] + ' $' if price_box else '-'
    item["rating"] = rating_box.text.strip() if rating_box else '-'
    item["date"] = ' '.join(date_box.text.strip().split(', ')) if date_box else '-'
    item["proc"] = proc_box.text.strip() if proc_box else '-'

    if name_box:
        item["model"] = name_box.text.strip()
        item["brand"] = name_box.text.strip().split()[0] 
    else:
        item["model"], item["brand"] = '-', '-'

    return item


def scrape_and_update_db():
    client = MongoClient('localhost', 27017)
    db = client['local']
    collection = db['phone']

    for brand in scrape_brands():
        for device in scrape_devices_from_brand(brand):
            print("Inserting device and sleeping 0.1 secs.")
            collection.insert_one(scrape_device_info(device))
            time.sleep(0.1)


scrape_and_update_db()
