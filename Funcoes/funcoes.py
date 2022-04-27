import requests
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Farmacias.Classes import Farmacia
import pandas as pd
import time
from datetime import date


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
        {'PRODUTO': [], 'LINK': [], 'MARCA': [], 'PREÇO CONSUMIDOR': [], 'PREÇO ORIGINAL': [],
         'PREÇO ATACADO': [], 'EAN': []}).to_csv(filename, sep=';', mode='w', index=False, encoding='utf-8')
    return None


def write_csv(names_temp: list, links_temp: list, brands_temp: list, prices_temp: list, old_prices_temp: list,
              wholesale_prices_temp: list, ean_temp: list, filename: str) -> None:
    pd.DataFrame(
        {'PRODUTO': names_temp, 'LINK': links_temp, 'MARCA': brands_temp, 'PRECO CONSUMIDOR': prices_temp,
         'PRECO ORIGINAL': old_prices_temp, 'PRECO ATACADO': wholesale_prices_temp, 'EAN': ean_temp}). \
        to_csv(filename, sep=';', mode='a', header=False, index=False)
    return None


def generate_data(company: Farmacia) -> None:
    """
    write the scrapped data to a file\n
    :param company: object from class Farmacia
    :return: None
    """

    time_string = date.today()
    write_header(company.filename.format(time_string))

    counter = 1
    for aba in company.tab_list:
        driver = get_driver(aba)
        time.sleep(2)

        scrape_all(driver=driver, title_xpath=company.titles_xpath,
                   brand_xpath=company.brand_xpath, old_price_xpath=company.old_price_xpath,
                   wholesale_price_xpath=company.wholesale_price_xpath, price_xpath=company.price_xpath,
                   price_xpath2=company.price_xpath2, ean_xpath=company.ean_xpath,
                   next_xpath=company.next_xpath, filename=company.filename.format(time_string),
                   url_xpath=company.url_xpath)

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


def scrape_all(driver, title_xpath: str, url_xpath: str, brand_xpath: str, old_price_xpath: str,
               wholesale_price_xpath: str,
               price_xpath: str, price_xpath2: str, ean_xpath: str,
               next_xpath: str, filename: str) -> None:
    """
    This function scrapes a desired website\n
    :param url_xpath: xpath to find urls of products listed in the page
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
    next_page = 2

    while True:
        print('Página ' + str(next_page - 1))
        names_temp, links_temp, brands_temp, old_prices_temp, wholesale_prices_temp, prices_temp, ean_temp = \
            get_page(driver, title_xpath=title_xpath, link_xpath=url_xpath, brand_xpath=brand_xpath,
                     old_price_xpath=old_price_xpath,
                     wholesale_price_xpath=wholesale_price_xpath,
                     price_xpath=price_xpath,
                     price_xpath2=price_xpath2,
                     ean_xpath=ean_xpath)

        write_csv(names_temp=names_temp, links_temp=links_temp, brands_temp=brands_temp,
                  old_prices_temp=old_prices_temp, wholesale_prices_temp=wholesale_prices_temp,
                  prices_temp=prices_temp, ean_temp=ean_temp,
                  filename=filename)

        print("\n" + "-" * 64)
        print(("Produtos encontrados: " + str(len(names_temp))).center(64))
        total += len(names_temp)
        print("-" * 64)
        print(("Total parcial de produtos: " + str(total)).center(64))
        print("-" * 64 + "\n")

        try:
            element = driver.find_element(by=By.XPATH, value=next_xpath.format(next_page))
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            element.click()
            next_page += 1

        except:
            print('Última página da aba atingida')
            break


def get_page(driver, title_xpath: str, link_xpath: str, brand_xpath: str, old_price_xpath: str,
             wholesale_price_xpath: str,
             price_xpath: str, price_xpath2: str, ean_xpath: str) -> tuple[list, list, list, list, list, list, list]:
    """
    Scrapes all names, brands, prices, EAN's and links of products listed in a single page\n
    :param link_xpath: xpath to all urls of product pages
    :param driver: driver which opens the browser
    :param title_xpath: XPATH to all the products in a page
    :param brand_xpath: XPATH to the name of the brand of a product
    :param old_price_xpath: XPATH to the original price, if applicable
    :param wholesale_price_xpath: XPATH to the wholesale price, if applicable
    :param price_xpath: XPATH to the actual price
    :param price_xpath2: alternate XPATH in case the first returns None
    :param ean_xpath: XPATH to EAN of a product
    :return: names, links, brands, old_prices, wholesale_prices, prices, ean
    """

    try:
        title_html = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, title_xpath)))
        # title_html = driver.find_elements(by=By.XPATH, value=title_xpath)
        urls_html = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, link_xpath)))
    # urls_html = driver.find_elements(by=By.XPATH, value=link_xpath)
    except TimeoutError:
        print("Elementos não localizados")

    names, links = get_titles(title_html, urls_html)
    brands, old_prices, wholesale_prices, prices, ean = get_attributes(links, brand_xpath=brand_xpath,
                                                                       old_price_xpath=old_price_xpath,
                                                                       wholesale_price_xpath=wholesale_price_xpath,
                                                                       price_xpath=price_xpath,
                                                                       price_xpath2=price_xpath2,
                                                                       ean_xpath=ean_xpath)

    return names, links, brands, old_prices, wholesale_prices, prices, ean


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
    i = 1

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}

    for link in links:
        req = requests.Session()
        html = req.get(url=link, headers=headers).content
        sel = Selector(text=html)

        # with open('xpath{}.txt'.format(i), 'w') as file:
        #     file.write(str(html))
        # i += 1

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


def get_titles(titles: list, links: list) -> tuple[list, list]:
    """
    Searches the names and links of all products in list of html files\n
    :param links: htmls which contain the link in "href" attribute
    :param titles: list of html files
    :return: names, urls
    """
    names = []
    urls = []
    i = 1

    for title, link in zip(titles, links):
        print('\nProduto ' + str(i) + ':')
        print(title.text)
        print(link.get_attribute('href'))
        names.append(title.text)
        urls.append(link.get_attribute('href'))
        i += 1

    return names, urls
