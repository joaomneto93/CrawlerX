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
        self.price_xpath = "//div[@class='price-info']//div[@class='price-box']/span/p[2]/span/span[2]/text()"
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
        lista_abas = ["/html/body/div[14]/div/header/div[2]/div/nav/ol/li[2]/a",
                      "//a[@href='https://www.drogaraia.com.br/bem-estar.html']",
                      "//a[@href='https://www.drogaraia.com.br/mamae-e-bebe.html']",
                      "//a[@href='https://www.drogaraia.com.br/beleza.html']",
                      "//a[@href='https://www.drogaraia.com.br/cabelo.html']",
                      "//a[@href='https://www.drogaraia.com.br/higiene-pessoal.html']"]

        nomes = []
        links = []
        marcas = []
        precos = []
        ean = []

        for aba in lista_abas:
            driver = self.get_driver()
            time.sleep(5)
            driver.find_element(by=By.XPATH, value=aba).click()
            nomes_temp, links_temp, marcas_temp, precos_temp, ean_temp = \
                scrape_all(driver=driver, title_xpath=self.titles_xpath,
                           marca_xpath=self.marca_xpath, price_xpath=self.price_xpath,
                           ean_xpath=self.ean_xpath, next_xpath=self.next_xpath)
            driver.quit()

            nomes.extend(nomes_temp)
            links.extend(links_temp)
            marcas.extend(marcas_temp)
            precos.extend(precos_temp)
            ean.extend(ean_temp)

        lista_produtos = pd.DataFrame(
            {'PRODUTO': nomes, 'LINK': links, 'MARCA': marcas, 'PRECO CONSUMIDOR': precos, 'EAN': ean})
        lista_produtos.to_csv('Arquivos/droga_raia.csv', sep=';')

