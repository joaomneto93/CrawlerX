import requests
from scrapy import Selector
from selenium.webdriver.common.by import By


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
