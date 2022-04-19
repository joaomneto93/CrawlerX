import requests
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time


def get_driver(url: str):
    """
    get the driver for a desired url\n
    :param url: url of the website
    :return: driver
    """
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("disable-infobars")
    options.add_argument('disable-dev-shm-usage')
    options.add_argument("no-sandbox")

    driver = webdriver.Chrome(service=Service("chromedriver_win32/chromedriver.exe"), options=options)
    driver.get(url)

    return driver


def generate_data(class_farmacia) -> None:
    """
    write the scrapped data to a file\n
    :param class_farmacia: class of the desired company
    :return: None
    """
    farmacia = class_farmacia()

    lista_produtos = pd.DataFrame(
        {'PRODUTO': [], 'LINK': [], 'MARCA': [], 'PRECO CONSUMIDOR': [], 'PRECO ORIGINAL': [],
         'PRECO ATACADO': [], 'EAN': []})
    lista_produtos.to_csv(farmacia.filename, sep=';', mode='w', index=False)

    counter = 1
    for aba in farmacia.lista_abas:
        driver = get_driver(aba)
        time.sleep(2)

        names_temp, links_temp, brands_temp, old_prices_temp, wholesale_prices_temp, precos_temp, ean_temp = \
            scrape_all(driver=driver, title_xpath=farmacia.titles_xpath,
                       brand_xpath=farmacia.brand_xpath, old_price_xpath=farmacia.old_price_xpath,
                       wholesale_price_xpath=farmacia.wholesale_price_xpath, price_xpath=farmacia.price_xpath,
                       price_xpath2=farmacia.price_xpath2, ean_xpath=farmacia.ean_xpath,
                       next_xpath=farmacia.next_xpath)

        driver.quit()

        pd.DataFrame(
            {'PRODUTO': names_temp, 'LINK': links_temp, 'MARCA': brands_temp, 'PRECO CONSUMIDOR': precos_temp,
             'PRECO ORIGINAL': old_prices_temp, 'PRECO ATACADO': wholesale_prices_temp, 'EAN': ean_temp}). \
            to_csv(farmacia.filename, sep=';', mode='a', header=False, index=False)

        print("\n" + "-" * 30)
        print(("Aba " + str(counter) + " concluída!").center(30))
        print("-" * 30 + "\n")
        counter += 1
        print("Produtos encontrados: " + str(len(names_temp)))

    print("\n" + "-" * 30)
    print("-" * 30)
    print("Extração concluída!".center(30))
    print("-" * 30)
    print("-" * 30 + "\n")
    return None


def scrape_all(driver, title_xpath: str, brand_xpath: str, old_price_xpath: str, wholesale_price_xpath: str,
               price_xpath: str, price_xpath2: str, ean_xpath: str,
               next_xpath: str) -> tuple[list, list, list, list, list, list, list]:
    """
    This function scrapes a desired website\n
    :param driver: driver which opens the browser
    :param title_xpath: XPATH to all the products in a page
    :param brand_xpath: XPATH to the name of the brand of a product
    :param old_price_xpath: XPATH to the original price, if applicable
    :param wholesale_price_xpath: XPATH to the wholesale price, if applicable
    :param price_xpath: XPATH to the actual price
    :param price_xpath2: alternate XPATH in case the first returns None
    :param ean_xpath: XPATH to EAN of a product
    :param next_xpath: XPATH to click on next page
    :return: names, links, brands, old_prices, wholesale_prices, precos, ean
    """

    names = []
    links = []
    brands = []
    old_prices = []
    wholesale_prices = []
    precos = []
    ean = []

    while True:
        names_temp, links_temp, brands_temp, old_prices_temp, wholesale_prices_temp, precos_temp, ean_temp = \
            get_page(driver, title_xpath=title_xpath, brand_xpath=brand_xpath, old_price_xpath=old_price_xpath,
                     wholesale_price_xpath=wholesale_price_xpath,
                     price_xpath=price_xpath,
                     price_xpath2=price_xpath2,
                     ean_xpath=ean_xpath)

        names.extend(names_temp)
        links.extend(links_temp)
        brands.extend(brands_temp)
        old_prices.extend(old_prices_temp)
        wholesale_prices.extend(wholesale_prices_temp)
        precos.extend(precos_temp)
        ean.extend(ean_temp)

        try:
            driver.find_element(by=By.XPATH, value=next_xpath).click()
        except:
            break

    return names, links, brands, old_prices, wholesale_prices, precos, ean


def get_page(driver, title_xpath: str, brand_xpath: str, old_price_xpath: str, wholesale_price_xpath: str,
             price_xpath: str, price_xpath2: str, ean_xpath: str) -> tuple[list, list, list, list, list, list, list]:
    """
    Scrapes all names, brands, prices, EAN's and links of products listed in a single page\n
    :param driver: driver which opens the browser
    :param title_xpath: XPATH to all the products in a page
    :param brand_xpath: XPATH to the name of the brand of a product
    :param old_price_xpath: XPATH to the original price, if applicable
    :param wholesale_price_xpath: XPATH to the wholesale price, if applicable
    :param price_xpath: XPATH to the actual price
    :param price_xpath2: alternate XPATH in case the first returns None
    :param ean_xpath: XPATH to EAN of a product
    :return: names, links, brands, old_prices, wholesale_prices, precos, ean
    """

    titles = driver.find_elements(by=By.XPATH, value=title_xpath)

    names, links = get_titles(titles)
    brands, old_prices, wholesale_prices, precos, ean = get_attributes(links, brand_xpath=brand_xpath,
                                                                       old_price_xpath=old_price_xpath,
                                                                       wholesale_price_xpath=wholesale_price_xpath,
                                                                       price_xpath=price_xpath,
                                                                       price_xpath2=price_xpath2,
                                                                       ean_xpath=ean_xpath)

    return names, links, brands, old_prices, wholesale_prices, precos, ean


def get_attributes(links: list, brand_xpath: str, old_price_xpath: str, wholesale_price_xpath: str, price_xpath: str,
                   price_xpath2: str, ean_xpath: str) -> tuple[list, list, list, list, list]:
    """
    Função que busca as brands, preços e EAN's de todos os produtos listados em uma página\n
    :param links: list of links of the products listed in a single page
    :param brand_xpath: XPATH to the name of the brand of a product
    :param old_price_xpath: XPATH to the original price, if applicable
    :param wholesale_price_xpath: XPATH to the wholesale price, if applicable
    :param price_xpath: XPATH to the actual price
    :param price_xpath2: alternate XPATH in case the first returns None
    :param ean_xpath: XPATH to EAN of a product
    :return: brands, old_prices, wholesale_prices, prices, ean
    """
    prices = []
    old_prices = []
    wholesale_prices = []
    ean = []
    brands = []

    for link in links:
        html = requests.get(url=link).content
        sel = Selector(text=html)

        brand = sel.xpath(brand_xpath).extract_first()

        old_price = sel.xpath(old_price_xpath).extract_first()

        wholesale_price = sel.xpath(wholesale_price_xpath).extract_first()

        if sel.xpath(price_xpath).extract_first() is None:
            price = sel.xpath(price_xpath2).extract_first()
        else:
            price = sel.xpath(price_xpath).extract_first()

        n_ean = sel.xpath(ean_xpath).extract_first()

        brands.append(brand)
        old_prices.append(old_price)
        wholesale_prices.append(wholesale_price)
        prices.append(price)
        ean.append(n_ean)

    return brands, old_prices, wholesale_prices, prices, ean


def get_titles(titles: list) -> tuple[list, list]:
    """
    Searches the names and links of all products in list of html files\n
    :param titles: list of html files
    :return: names, links
    """
    names = []
    links = []

    for i, title in enumerate(titles):
        print('\nProduto ' + str(i + 1) + ':')
        print(title.text)
        names.append(title.text)
        links.append(title.get_attribute('href'))

    return names, links
