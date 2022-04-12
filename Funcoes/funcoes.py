import requests
from scrapy import Selector
from selenium.webdriver.common.by import By


def get_page(driver, title_xpath: str, marca_xpath: str, price_xpath: str, ean_xpath: str) -> tuple[list, list, list,
                                                                                                    list, list]:
    """
    Função que "raspa"(scrape) todos os nomes, marcas, preços, EAN's e os respectivos links dos remédios listados em uma
    única página\n
    :param driver: o driver utilizado para abrir o navegador
    :param title_xpath: XPATH para todos os remédios listados em uma página
    :param marca_xpath: XPATH da string da marca na página do produto
    :param price_xpath: XPATH do preço na página do produto
    :param ean_xpath: XPATH do EAN na página do produto
    :return: tuple com cinco listas com os nomes, links, marcas, preços e EAN's (respectivamente) de todos os produtos listados em uma página
    """
    titles = driver.find_elements(by=By.XPATH, value=(
        title_xpath))

    print("Products found: " + str(len(titles)))
    nomes, links = get_titles(titles)
    marcas, precos, ean = get_attributes(links, marca_xpath=marca_xpath, price_xpath=price_xpath, ean_xpath=ean_xpath)
    return nomes, links, marcas, precos, ean


def get_titles(titles: list) -> tuple[list, list]:
    """
    Função que busca os nomes e links de todos os produtos em uma lista de elementos html\n
    :param titles: lista de elementos html
    :return: tuple com duas listas, equivalentes aos nomes e links de todos os elementos html listados
    """
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


def get_attributes(links: list, marca_xpath: str, price_xpath: str, ean_xpath: str) -> tuple[list, list, list]:
    """
    Função que busca as marcas, preços e EAN's de todos os produtos listados em uma página\n
    :param links: lista de links dos produtos presentes em uma página
    :param marca_xpath: XPATH que leva à string da marca
    :param price_xpath: XPATH que leva à string do preço
    :param ean_xpath: XPATH que leva à string do EAN
    :return: tuple de três listas com as marcas, preços e EAN's respectivos aos links inputados
    """
    prices = []
    ean = []
    marcas = []

    for link in links:
        print(link)
        html = requests.get(url=link).content
        sel = Selector(text=html)
        marca = sel.xpath(marca_xpath).get()
        price = sel.xpath(price_xpath).extract_first()
        n_ean = sel.xpath(ean_xpath).extract_first()
        marcas.append(marca)
        prices.append(price)
        ean.append(n_ean)
        print(marca)
        print(price)
        print(n_ean)

    return marcas, prices, ean


def scrape_all(driver, title_xpath: str, marca_xpath: str, price_xpath: str, ean_xpath: str, next_xpath: str) -> \
        tuple[list, list, list, list, list]:
    """
    Função para "raspagem" (scrapping) ao longo de todas as páginas de um site\n
    :param driver: o driver utilizado para abrir o navegador
    :param title_xpath: XPATH para todos os remédios listados em uma página
    :param marca_xpath: XPATH da string da marca na página do produto
    :param price_xpath: XPATH do preço na página do produto
    :param ean_xpath: XPATH do EAN na página do produto
    :param next_xpath: XPATH para o clique na página seguinte
    :return: tuple com cinco listas com os nomes, links, marcas, preços e EAN's (respectivamente) de todos os produtos listados em um site
    """

    nomes = []
    links = []
    marcas = []
    precos = []
    ean = []

    while True:
        nomes_temp, links_temp, marcas_temp, precos_temp, ean_temp = get_page(driver, title_xpath=title_xpath,
                                                                              marca_xpath=marca_xpath,
                                                                              price_xpath=price_xpath,
                                                                              ean_xpath=ean_xpath)

        nomes.extend(nomes_temp)
        links.extend(links_temp)
        marcas.extend(marcas_temp)
        precos.extend(precos_temp)
        ean.extend(ean_temp)

        try:
            driver.find_element(by=By.XPATH,
                                value=next_xpath).click()
        except:
            break

    return nomes, links, marcas, precos, ean
