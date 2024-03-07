import requests
from bs4 import BeautifulSoup

with open("mutual_funds_links.txt", 'w') as f:

    page = requests.get("https://groww.in/mutual-funds/filter?q=&fundSize=&investType=%5B%22SIP%22%5D&sortBy=3")

    soup = BeautifulSoup(page.text, 'html.parser')

    rows = soup.find_all('a', attrs={'class': 'pos-rel f22Link'})

    for row in rows:
        f.write(f"https://groww.in{row.get('href')}\n")

    for page_number in range(1, 94):

        page = requests.get(f"https://groww.in/mutual-funds/filter?q=&fundSize=&investType=%5B%22SIP%22%5D&pageNo={page_number}&sortBy=3")

        soup = BeautifulSoup(page.text, 'html.parser')

        rows = soup.find_all('a', attrs={'class': 'pos-rel f22Link'})

        for row in rows:
            f.write(f"https://groww.in{row.get('href')}\n")