from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import time

c = webdriver.ChromeOptions()
c.add_argument('--headless')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=c)

df = pd.DataFrame(
    columns=['Fund Name', 'Fund Type', 'AUM', 'Expense Ratio', 'Avg. Return %', 'P/E Ratio', 'P/B Ratio', 'Alpha',
             'Beta', 'Sharpe', 'Sortino'])

with open('mutual_funds_links.txt', 'r') as f:
    urls = f.read().split('\n')

for row_num, url in enumerate(urls):

    df_row = []

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

    soup = BeautifulSoup(page, 'html.parser')

    try:
        fund_name = soup.find('h1', attrs={'class': 'mfh239SchemeName displaySmall'}).text
        df_row.append(fund_name)

        if len(soup.find_all('div', attrs={'class': 'mfh239PillsContainer'})) > 1:
            fund_type = soup.find_all('div', attrs={'class': 'mfh239PillsContainer'})[1].text
            df_row.append(fund_type)
        else:
            df_row.append("NA")

        if soup.find_all('table', attrs={'class': 'tb10Table fd12Table'})[1].find_all('tr')[1] is not None:
            aum = soup.find_all('table', attrs={'class': 'tb10Table fd12Table'})[1].find_all('tr')[1].find_all('td')[1].text
            df_row.append(aum)
        else:
            df_row.append("NA")

        if soup.find('div', attrs={'class': 'mf320Heading'}) is not None:
            expense_ratio = soup.find('div', attrs={'class': 'mf320Heading'}).text
            expense_ratio = expense_ratio.split(':')[1].replace('Inclusive of GST', '').strip()
            df_row.append(expense_ratio)
        else:
            df_row.append("NA")

        if soup.find('div', attrs={'class': 'returns961TableContainer'}) is not None:
            th = soup.find('div', attrs={'class': 'returns961TableContainer'}).find_all('th', attrs={
                'class': 'contentSecondary bodyBaseHeavy'})
            th = [h.text for h in th]
            ind = th.index('All')

            avg_returns = soup.find_all('td', attrs={'class': 'tb10Td'})[ind].text
            df_row.append(avg_returns)
        else:
            df_row.append("NA")

        if soup.find('table', attrs={'class': 'tb10Table ha384Table col l5'}) is not None:
            pe_ratio = soup.find('table', attrs={'class': 'tb10Table ha384Table col l5'}).find_all('tr')[2].find('td').text
            df_row.append(pe_ratio)

            pb_ratio = soup.find('table', attrs={'class': 'tb10Table ha384Table col l5'}).find_all('tr')[3].find('td').text
            df_row.append(pb_ratio)
        else:
            df_row.append("NA")
            df_row.append("NA")

        if soup.find('table', attrs={'class': 'tb10Table ha384Table ha384TableRight col l5'}) is not None:
            alpha = soup.find('table', attrs={'class': 'tb10Table ha384Table ha384TableRight col l5'}).find_all('tr')[
                0].find('td').text
            df_row.append(alpha)

            beta = soup.find('table', attrs={'class': 'tb10Table ha384Table ha384TableRight col l5'}).find_all('tr')[
                1].find('td').text
            df_row.append(beta)

            sharpe = soup.find('table', attrs={'class': 'tb10Table ha384Table ha384TableRight col l5'}).find_all('tr')[
                2].find('td').text
            df_row.append(sharpe)

            sortino = soup.find('table', attrs={'class': 'tb10Table ha384Table ha384TableRight col l5'}).find_all('tr')[
                3].find('td').text
            df_row.append(sortino)
        else:
            df_row.append("NA")
            df_row.append("NA")
            df_row.append("NA")
            df_row.append("NA")

        df.loc[row_num] = df_row
        print(f"{fund_name}")

    except:
        print(f"{url} data could not be added")

df.to_excel(f'mutual_funds_details_{datetime.now().strftime("%d-%m-%Y")}.xlsx', index=False)
