import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from scrapy import Selector


class DrogaRaia():

    def __init__(self):
        self.url = "https://www.drogaraia.com.br/"

    def get_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("disable-infobars")
        options.add_argument('disable-dev-shm-usage')
        options.add_argument("no-sandbox")

        driver = webdriver.Chrome(service=Service("chromedriver_win32/chromedriver.exe"), options=options)
        driver.get(self.url)

        return driver

    def get_titles(self, titles):
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

    def get_prices_ean(self, links):
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

    def get_page(self, driver):
        titles = driver.find_elements(by=By.XPATH, value=(
            "//div[@class='product-info']/div[@class='product-name']/a[@class='show-hover']"))

        print("Products found: " + str(len(titles)))

        nomes, links = self.get_titles(titles)

        precos, ean = self.get_prices_ean(links)

        return nomes, links, precos, ean

    def scrape_all(self, driver):
        driver.find_element(by=By.XPATH, value="/html/body/div[14]/div/header/div[2]/div/nav/ol/li[2]/a").click()

        nomes = []
        links = []
        precos = []
        ean = []

        while True:
            nomes_temp, links_temp, precos_temp, ean_temp = self.get_page(driver)

            nomes.extend(nomes_temp)
            links.extend(links_temp)
            precos.extend(precos_temp)
            ean.extend(ean_temp)

            try:
                driver.find_element(by=By.XPATH,
                                    value='//a[@title="Próximo"]').click()
            except:
                break

        return nomes, links, precos, ean

    def generate_data(self):
        driver = self.get_driver()

        time.sleep(5)

        nomes, links, precos, ean = self.scrape_all(driver)

        lista_produtos = pd.DataFrame({'PRODUTO': nomes, 'LINK': links, 'PRECO CONSUMIDOR': precos, 'EAN': ean})

        # driver.find_element(by=By.XPATH, value="/html/body/div[9]/div/header/div[2]/div/nav/ol/li[3]/a").click()

        lista_produtos.to_csv('droga_raia.csv', sep=';')

        driver.quit()
