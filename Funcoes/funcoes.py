import requests
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from Farmacias.Classes import Farmacia
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


def write_header(filename: str) -> None:
    pd.DataFrame(
        {'PRODUTO': [], 'LINK': [], 'MARCA': [], 'PRECO CONSUMIDOR': [], 'PRECO ORIGINAL': [],
         'PRECO ATACADO': [], 'EAN': []}).to_csv(filename, sep=';', mode='w', index=False)
    return None


def write_csv(names_temp: list, links_temp: list, brands_temp: list, precos_temp: list, old_prices_temp: list,
              wholesale_prices_temp: list, ean_temp: list, filename: str) -> None:
    pd.DataFrame(
        {'PRODUTO': names_temp, 'LINK': links_temp, 'MARCA': brands_temp, 'PRECO CONSUMIDOR': precos_temp,
         'PRECO ORIGINAL': old_prices_temp, 'PRECO ATACADO': wholesale_prices_temp, 'EAN': ean_temp}). \
        to_csv(filename, sep=';', mode='a', header=False, index=False)
    return None


def generate_data(company: Farmacia) -> None:
    """
    write the scrapped data to a file\n
    :param company: object from class Farmacia
    :return: None
    """

    write_header(company.filename)

    counter = 1
    for aba in company.tab_list:
        driver = get_driver(aba)
        time.sleep(2)

        scrape_all(driver=driver, title_xpath=company.titles_xpath,
                   brand_xpath=company.brand_xpath, old_price_xpath=company.old_price_xpath,
                   wholesale_price_xpath=company.wholesale_price_xpath, price_xpath=company.price_xpath,
                   price_xpath2=company.price_xpath2, ean_xpath=company.ean_xpath,
                   next_xpath=company.next_xpath, filename=company.filename)

        print("\n" + "-" * 30)
        print(("Aba " + str(counter) + " concluída!").center(30))
        print("-" * 30 + "\n")
        counter += 1

        driver.quit()

    print("\n" + "-" * 30)
    print("-" * 30)
    print("Extração concluída!".center(30))
    print("-" * 30)
    print("-" * 30 + "\n")

    return None


def scrape_all(driver, title_xpath: str, brand_xpath: str, old_price_xpath: str, wholesale_price_xpath: str,
               price_xpath: str, price_xpath2: str, ean_xpath: str,
               next_xpath: str, filename: str) -> None:
    """
    This function scrapes a desired website\n
    :param filename: name of file to write to
    :param driver: driver which opens the browser
    :param title_xpath: XPATH to all the products in a page
    :param brand_xpath: XPATH to the name of the brand of a product
    :param old_price_xpath: XPATH to the original price, if applicable
    :param wholesale_price_xpath: XPATH to the wholesale price, if applicable
    :param price_xpath: XPATH to the actual price
    :param price_xpath2: alternate XPATH in case the first returns None
    :param ean_xpath: XPATH to EAN of a product
    :param next_xpath: XPATH to click on next page
    :return: None
    """

    total = 0

    while True:
        names_temp, links_temp, brands_temp, old_prices_temp, wholesale_prices_temp, precos_temp, ean_temp = \
            get_page(driver, title_xpath=title_xpath, brand_xpath=brand_xpath, old_price_xpath=old_price_xpath,
                     wholesale_price_xpath=wholesale_price_xpath,
                     price_xpath=price_xpath,
                     price_xpath2=price_xpath2,
                     ean_xpath=ean_xpath)

        write_csv(names_temp=names_temp, links_temp=links_temp, brands_temp=brands_temp,
                  old_prices_temp=old_prices_temp, wholesale_prices_temp=wholesale_prices_temp,
                  precos_temp=precos_temp, ean_temp=ean_temp,
                  filename=filename)

        print("\n" + "-" * 64)
        print(("Produtos encontrados: " + str(len(names_temp))).center(64))
        total += len(names_temp)
        print("-" * 64)
        print(("Total parcial de produtos: " + str(total)).center(64))
        print("-" * 64 + "\n")

        try:
            driver.find_element(by=By.XPATH, value=next_xpath).click()
        except:
            break

    return None


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

        brand = str(sel.xpath(brand_xpath).extract_first()).strip()

        old_price = str(sel.xpath(old_price_xpath).extract_first()).strip()

        wholesale_price = str(sel.xpath(wholesale_price_xpath).extract_first()).strip()

        if sel.xpath(price_xpath).extract_first() is None:
            price = str(sel.xpath(price_xpath2).extract_first()).strip()
        else:
            price = str(sel.xpath(price_xpath).extract_first()).strip()

        n_ean = str(sel.xpath(ean_xpath).extract_first()).strip()

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
