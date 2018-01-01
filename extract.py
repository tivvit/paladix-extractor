import csv
import json
import re
import requests
from pyquery import PyQuery as pq


def get_paladix(url):
    r = requests.get(url)

    d = pq(r.text)
    ad = d(".list-ads-row")

    header = ad(".list-ads-name").text()
    text = ad(".list-ads-row-content").text()[len(header):]
    date = ad(".list-ads-header").text().split('|')[3].strip() \
        .replace("vloženo: ", "")
    price_search = re.search(r"(cena|Cena){1}:? *([0-9 ]+){1}", text).group(
        2).replace(" ", "")
    price = int(price_search if price_search else 0)
    mail = ad(".list-ads-footer a").eq(0).text()
    phone_search = re.search(r"tel.: ([0-9 ]{9})",
                             ad(".list-ads-footer").text())
    phone = phone_search.group(1) if phone_search else ""

    return {
        "price": price,
        "mail": mail,
        "phone": phone,
        "header": header,
        "text": text,
        "date": date,
        "url": url,
    }


if __name__ == "__main__":
    pages = []
    with open("/app/links", "r") as f:
        for i in f:
            l = i.strip()
            pages.append(get_paladix(l))

    with open('/app/data.csv', 'w') as csvfile:
        # d = csv.Dialect
        # d.delimiter = ';'
        writer = csv.DictWriter(csvfile, fieldnames=pages[0].keys())
        # csv.register_dialect('semi', delimiter=';', quoting=csv.QUOTE_NONE)
        writer.writeheader()
        for i in pages:
            writer.writerow(i)
