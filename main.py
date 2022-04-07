from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import requests


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobars")
    options.add_argument('disable-dev-shm-usage')
    options.add_argument("no-sandbox")

    driver = webdriver.Chrome(service=Service("chromedriver_win32/chromedriver.exe"), options=options)
    driver.get("https://www.drogaraia.com.br/")
    return driver


def raia():
    nomes = []
    driver = get_driver()
    time.sleep(5)

    driver.find_element(by=By.XPATH, value="/html/body/div[14]/div/header/div[2]/div/nav/ol/li[2]/a").click()

    titles = driver.find_elements(by=By.XPATH, value=("//*[@class='product-info']"))

    for i, title in enumerate(titles):
        print('Produto ' + str(i + 1) + ':\n')
        print(title.text)
        print('\n')
        nomes.append(title.text.replace('\n', ';'))

    print("Products found: " + str(len(titles)))

    print(nomes)

    driver.find_element(by=By.XPATH, value="/html/body/div[9]/div/header/div[2]/div/nav/ol/li[3]/a").click()
    driver.quit()
    return nomes


if __name__ == '__main__':
    print('Static text running')
    lista1 = raia()
    with open('droga_raia.csv', 'w') as file:
        for element in lista1:
            file.write(str(element))
            file.write('\n')
