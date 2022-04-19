import requests
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time


def get_driver(url):
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    options.add_argument("disable-infobars")
    options.add_argument('disable-dev-shm-usage')
    options.add_argument("no-sandbox")

    driver = webdriver.Chrome(service=Service("chromedriver_win32/chromedriver.exe"), options=options)
    driver.get(url)

    return driver


def generate_data(class_farmacia):
    farmacia = class_farmacia()

    lista_produtos = pd.DataFrame(
        {'PRODUTO': [], 'LINK': [], 'MARCA': [], 'PRECO CONSUMIDOR': [], 'PRECO ORIGINAL': [],
         'PRECO ATACADO': [], 'EAN': []})
    lista_produtos.to_csv(farmacia.filename, sep=';', mode='w', index=False)

    counter = 1
    for aba in farmacia.lista_abas:
        driver = get_driver(aba)
        time.sleep(2)

        nomes_temp, links_temp, marcas_temp, precos_antigos_temp, precos_promo_temp, precos_temp, ean_temp = \
            scrape_all(driver=driver, title_xpath=farmacia.titles_xpath,
                       marca_xpath=farmacia.marca_xpath, old_price_xpath=farmacia.old_price_xpath,
                       promo_price_xpath=farmacia.promo_price_xpath, price_xpath=farmacia.price_xpath,
                       price_xpath2=farmacia.price_xpath2, ean_xpath=farmacia.ean_xpath,
                       next_xpath=farmacia.next_xpath)

        driver.quit()

        pd.DataFrame(
            {'PRODUTO': nomes_temp, 'LINK': links_temp, 'MARCA': marcas_temp, 'PRECO CONSUMIDOR': precos_temp,
             'PRECO ORIGINAL': precos_antigos_temp, 'PRECO ATACADO': precos_promo_temp, 'EAN': ean_temp}). \
            to_csv(farmacia.filename, sep=';', mode='a', header=False, index=False)

        print("\n" + "-" * 30)
        print(("Aba " + str(counter) + " concluída!").center(30))
        print("-" * 30 + "\n")
        counter += 1

    print("\n"+"-"*30)
    print("-"*30)
    print("Extração concluída!".center(30))
    print("-"*30)
    print("-"*30+"\n")
    return None


def scrape_all(driver, title_xpath: str, marca_xpath: str, old_price_xpath: str, promo_price_xpath: str,
               price_xpath: str, price_xpath2: str, ean_xpath: str,
               next_xpath: str) -> tuple[list, list, list, list, list, list, list]:
    """
    Função para "raspagem" (scrapping) ao longo de todas as páginas de um site\n
    :param driver: o driver utilizado para abrir o navegador
    :param title_xpath: XPATH para todos os remédios listados em uma página
    :param marca_xpath: XPATH da string da marca na página do produto
    :param old_price_xpath: XPATH para o preço original, se existir
    :param promo_price_xpath: XPATH para o preço de atacado, se existir
    :param price_xpath: XPATH do preço na página do produto
    :param price_xpath2: XPATH alternativo caso o inicial retorne None
    :param ean_xpath: XPATH do EAN na página do produto
    :param next_xpath: XPATH para o clique na página seguinte
    :return: nomes, links, marcas, precos_antigos, precos_promo, precos, ean
    """

    nomes = []
    links = []
    marcas = []
    precos_antigos = []
    precos_promo = []
    precos = []
    ean = []

    while True:
        nomes_temp, links_temp, marcas_temp, precos_antigos_temp, precos_promo_temp, precos_temp, ean_temp = \
            get_page(driver, title_xpath=title_xpath, marca_xpath=marca_xpath, old_price_xpath=old_price_xpath,
                     promo_price_xpath=promo_price_xpath,
                     price_xpath=price_xpath,
                     price_xpath2=price_xpath2,
                     ean_xpath=ean_xpath)

        nomes.extend(nomes_temp)
        links.extend(links_temp)
        marcas.extend(marcas_temp)
        precos_antigos.extend(precos_antigos_temp)
        precos_promo.extend(precos_promo_temp)
        precos.extend(precos_temp)
        ean.extend(ean_temp)

        try:
            driver.find_element(by=By.XPATH, value=next_xpath).click()
        except:
            break

    return nomes, links, marcas, precos_antigos, precos_promo, precos, ean


def get_page(driver, title_xpath: str, marca_xpath: str, old_price_xpath: str, promo_price_xpath: str, price_xpath: str,
             price_xpath2: str, ean_xpath: str) -> tuple[list, list, list, list, list, list, list]:
    """
    Função que "raspa"(scrape) todos os nomes, marcas, preços, EAN's e os respectivos links dos remédios listados em uma
    única página\n
    :param driver: o driver utilizado para abrir o navegador
    :param title_xpath: XPATH para todos os remédios listados em uma página
    :param marca_xpath: XPATH da string da marca na página do produto
    :param old_price_xpath: XPATH para o preço original, se existir
    :param promo_price_xpath: XPATH para o preço de atacado, se existir
    :param price_xpath: XPATH do preço na página do produto
    :param price_xpath2: XPATH alternativo caso o inicial retorne None
    :param ean_xpath: XPATH do EAN na página do produto
    :return: nomes, links, marcas, precos_antigos, precos_atacado, precos, ean
    """

    titles = driver.find_elements(by=By.XPATH, value=title_xpath)

    print("Products found: " + str(len(titles)))
    nomes, links = get_titles(titles)
    marcas, precos_antigos, precos_atacado, precos, ean = get_attributes(links, marca_xpath=marca_xpath,
                                                                         old_price_xpath=old_price_xpath,
                                                                         promo_price_xpath=promo_price_xpath,
                                                                         price_xpath=price_xpath,
                                                                         price_xpath2=price_xpath2,
                                                                         ean_xpath=ean_xpath)

    return nomes, links, marcas, precos_antigos, precos_atacado, precos, ean


def get_attributes(links: list, marca_xpath: str, old_price_xpath: str, promo_price_xpath: str, price_xpath: str,
                   price_xpath2: str, ean_xpath: str) -> tuple[list, list, list, list, list]:
    """
    Função que busca as marcas, preços e EAN's de todos os produtos listados em uma página\n
    :param links: lista de links dos produtos presentes em uma página
    :param marca_xpath: XPATH que leva à string da marca
    :param old_price_xpath: XPATH para o preço original, se existir
    :param promo_price_xpath: XPATH para o preço de atacado, se existir
    :param price_xpath2: XPATH alternativo caso o inicial retorne None
    :param price_xpath: XPATH que leva à string do preço
    :param ean_xpath: XPATH que leva à string do EAN
    :return: marcas, old_prices, promo_prices, prices, ean
    """
    prices = []
    old_prices = []
    promo_prices = []
    ean = []
    marcas = []

    for link in links:
        html = requests.get(url=link).content
        sel = Selector(text=html)

        marca = sel.xpath(marca_xpath).extract_first()

        old_price = sel.xpath(old_price_xpath).extract_first()

        promo_price = sel.xpath(promo_price_xpath).extract_first()

        if sel.xpath(price_xpath).extract_first() is None:
            price = sel.xpath(price_xpath2).extract_first()
        else:
            price = sel.xpath(price_xpath).extract_first()

        n_ean = sel.xpath(ean_xpath).extract_first()

        marcas.append(marca)
        old_prices.append(old_price)
        promo_prices.append(promo_price)
        prices.append(price)
        ean.append(n_ean)

    return marcas, old_prices, promo_prices, prices, ean


def get_titles(titles: list) -> tuple[list, list]:
    """
    Função que busca os nomes e links de todos os produtos em uma lista de elementos html\n
    :param titles: lista de elementos html
    :return: nomes, links
    """
    nomes = []
    links = []

    for i, title in enumerate(titles):
        print('\nProduto ' + str(i + 1) + ':')
        print(title.text)
        nomes.append(title.text)
        links.append(title.get_attribute('href'))

    return nomes, links
