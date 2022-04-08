from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import numpy as np
from scrapy import Selector
import requests
import pandas as pd
import time


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobars")
    options.add_argument('disable-dev-shm-usage')
    options.add_argument("no-sandbox")

    driver = webdriver.Chrome(service=Service("chromedriver_win32/chromedriver.exe"), options=options)
    driver.get("https://www.drogaraia.com.br/")
    return driver


def get_titles(titles):
    nomes = []
    links = []
    for i, title in enumerate(titles):
        print('Produto ' + str(i + 1) + ':\n')
        print(title)
        print(title.text)
        print(title.get_attribute('href'))
        print('\n')
        nomes.append(title.text)
        links.append(title.get_attribute('href'))
    return nomes, links


def get_prices_ean(links):
    prices = []
    ean = []
    for link in links:
        print(link)
        html = requests.get(url=link).content
        sel = Selector(text=html)
        price = sel.xpath("//span[@class='price']/span[2]/text()").get()
        n_ean = sel.xpath("//*[@id='product-attribute-specs-table']/tbody/tr[2]/td/text()").get()
        prices.append(price)
        ean.append(n_ean)
        print(price)
        print(n_ean)
    return prices, ean


def raia():
    driver = get_driver()
    time.sleep(5)

    driver.find_element(by=By.XPATH, value="/html/body/div[14]/div/header/div[2]/div/nav/ol/li[2]/a").click()

    titles = driver.find_elements(by=By.XPATH, value=(
        "//div[@class='product-info']/div[@class='product-name']/a[@class='show-hover']"))

    print("Products found: " + str(len(titles)))

    nomes, links = get_titles(titles)

    precos,ean = get_prices_ean(links)

    produtos = pd.DataFrame({'PRODUTO': nomes, 'LINK': links, 'CUSTO': precos, 'EAN': ean})

    # driver.find_element(by=By.XPATH, value="/html/body/div[9]/div/header/div[2]/div/nav/ol/li[3]/a").click()
    driver.quit()
    return produtos


if __name__ == '__main__':
    print('Static text running')
    lista_produtos = raia()
    print(lista_produtos)
    lista_produtos.to_csv('droga_raia.csv', sep=';')
