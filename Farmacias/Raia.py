import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from scrapy import Selector
from Funcoes.funcoes import *


class DrogaRaia():

    def __init__(self):
        self.url = "https://www.drogaraia.com.br/"
        self.marca_xpath = "//div[@class='product-attributes']//li[@class='marca show-hover']/text()"
        self.price_xpath = "//span[@class='price']/span[2]/text()"
        self.ean_xpath = "//*[@id='product-attribute-specs-table']/tbody/tr[2]/td/text()"
        self.titles_xpath = "//div[@class='product-info']/div[@class='product-name']/a[@class='show-hover']"
        self.next_xpath = '//a[@title="Próximo"]'

    def get_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("disable-infobars")
        options.add_argument('disable-dev-shm-usage')
        options.add_argument("no-sandbox")

        driver = webdriver.Chrome(service=Service("chromedriver_win32/chromedriver.exe"), options=options)
        driver.get(self.url)

        return driver

    def generate_data(self):
        driver = self.get_driver()
        time.sleep(5)
        driver.find_element(by=By.XPATH, value="/html/body/div[14]/div/header/div[2]/div/nav/ol/li[2]/a").click()
        nomes, links, marcas, precos, ean = scrape_all(driver=driver, title_xpath=self.titles_xpath,
                                                       marca_xpath=self.marca_xpath, price_xpath=self.price_xpath,
                                                       ean_xpath=self.ean_xpath,next_xpath=self.next_xpath)

        lista_produtos = pd.DataFrame(
            {'PRODUTO': nomes, 'LINK': links, 'MARCA': marcas, 'PRECO CONSUMIDOR': precos, 'EAN': ean})
        # driver.find_element(by=By.XPATH, value="/html/body/div[9]/div/header/div[2]/div/nav/ol/li[3]/a").click()
        lista_produtos.to_csv('Arquivos/droga_raia.csv', sep=';')
        driver.quit()
