from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

c = webdriver.ChromeOptions()
c.add_argument('--headless')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=c)

df = pd.DataFrame(
    columns=['Fund Name', 'Fund Type', 'AUM', 'Expense Ratio', 'P/E Ratio', 'P/B Ratio', 'Alpha', 'Beta', 'Sharpe', 'Sortino'])

with open('sample_funds.txt', 'r') as f:
    urls = f.read().split('\n')

for row_num, url in enumerate(urls):

    driver.get(url.strip())

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(1)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    page = driver.page_source

    # page = requests.get("https://groww.in/mutual-funds/parag-parikh-long-term-value-fund-direct-growth")

    soup = BeautifulSoup(page, 'html.parser')

    fund_name = soup.find('h1', attrs={'class': 'mfh239SchemeName displaySmall'}).text
    fund_type = soup.find_all('div', attrs={'class': 'mfh239PillsContainer'})[1].text

    aum = soup.find_all('table', attrs={'class': 'tb10Table fd12Table'})[1].find_all('tr')[1].find_all('td')[1].text

    expense_ratio = soup.find('div', attrs={'class': 'mf320Heading'}).text
    expense_ratio = expense_ratio.split(':')[1].replace('Inclusive of GST', '').strip()

    pe_ratio = soup.find('table', attrs={'class': 'tb10Table ha384Table col l5'}).find_all('tr')[2].find('td').text
    pb_ratio = soup.find('table', attrs={'class': 'tb10Table ha384Table col l5'}).find_all('tr')[3].find('td').text
    alpha = soup.find('table', attrs={'class': 'tb10Table ha384Table ha384TableRight col l5'}).find_all('tr')[0].find(
        'td').text
    beta = soup.find('table', attrs={'class': 'tb10Table ha384Table ha384TableRight col l5'}).find_all('tr')[1].find(
        'td').text
    sharpe = soup.find('table', attrs={'class': 'tb10Table ha384Table ha384TableRight col l5'}).find_all('tr')[2].find(
        'td').text
    sortino = soup.find('table', attrs={'class': 'tb10Table ha384Table ha384TableRight col l5'}).find_all('tr')[3].find(
        'td').text

    df.loc[row_num] = (
        [fund_name, fund_type, aum, expense_ratio, pe_ratio, pb_ratio, alpha, beta, sharpe, sortino])

    print(f"{fund_name} data added")

df.to_excel('sample_funds_data.xlsx', index=False)
