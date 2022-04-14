import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from scrapy import Selector
from Funcoes.funcoes import *


def get_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("disable-infobars")
    options.add_argument('disable-dev-shm-usage')
    options.add_argument("no-sandbox")

    driver = webdriver.Chrome(service=Service("chromedriver_win32/chromedriver.exe"), options=options)
    driver.get(url)

    return driver


class DrogaRaia:

    def __init__(self):
        self.lista_abas = ["https://www.drogaraia.com.br/medicamentos.html?limit=48",
                      "https://www.drogaraia.com.br/bem-estar.html?limit=48",
                      "https://www.drogaraia.com.br/mamae-e-bebe.html?limit=48",
                      "https://www.drogaraia.com.br/beleza.html?limit=48",
                      "https://www.drogaraia.com.br/cabelo.html?limit=48",
                      "https://www.drogaraia.com.br/higiene-pessoal.html?limit=48"]
        self.marca_xpath = "//div[@class='product-attributes']//li[@class='marca show-hover']/text()"
        self.old_price_xpath = "//div[@class='price-info']//div[@class='price-box']/span//p[@class='old-price']/span[2]/text()[2]"
        self.promo_price_xpath = "//div[@class='product_label raia-arrasa']//span[@class='price']/text()"
        self.price_xpath = "//div[@class='price-info']//div[@class='price-box']//p[@class='special-price']/" \
                           "span/span[2]/text()"
        self.price_xpath2 = "//div[@class='price-info']//div[@class='price-box']//span[@class='regular-price ']/" \
                            "span[2]/text()"
        self.ean_xpath = "//*[@id='product-attribute-specs-table']/tbody/tr[2]/td/text()"
        self.titles_xpath = "//div[@class='product-info']/div[@class='product-name']/a[@class='show-hover']"
        self.next_xpath = '//a[@title="Próximo"]'

    def generate_data(self):
        lista_produtos = pd.DataFrame(
            {'PRODUTO': [], 'LINK': [], 'MARCA': [], 'PRECO CONSUMIDOR': [], 'PRECO ORIGINAL': [],
             'PRECO ATACADO': [], 'EAN': []})
        lista_produtos.to_csv('Arquivos/droga_raia.csv', sep=';', mode='w', index=False)

        for aba in self.lista_abas:
            driver = get_driver(aba)
            time.sleep(2)

            # driver.find_element(by=By.XPATH, value=aba).click()

            nomes_temp, links_temp, marcas_temp, precos_antigos_temp, precos_promo_temp, precos_temp, ean_temp = \
                scrape_all(driver=driver, title_xpath=self.titles_xpath,
                           marca_xpath=self.marca_xpath, old_price_xpath=self.old_price_xpath,
                           promo_price_xpath=self.promo_price_xpath, price_xpath=self.price_xpath,
                           price_xpath2=self.price_xpath2, ean_xpath=self.ean_xpath, next_xpath=self.next_xpath)

            driver.quit()

            pd.DataFrame(
                {'PRODUTO': nomes_temp, 'LINK': links_temp, 'MARCA': marcas_temp, 'PRECO CONSUMIDOR': precos_temp,
                 'PRECO ORIGINAL': precos_antigos_temp, 'PRECO ATACADO': precos_promo_temp, 'EAN': ean_temp}). \
                to_csv('Arquivos/droga_raia.csv', sep=';', mode='a', header=False, index=False)
