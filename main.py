from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument('disable-dev-shm-usage')
    options.add_argument("no-sandbox")

    driver = webdriver.Chrome(service=Service("chromedriver_win32/chromedriver.exe"), options=options)
    driver.get("https://www.drogaraia.com.br/")
    return driver


def main():
    driver = get_driver()
    time.sleep(3)
    medicamentos = driver.find_element(by=By.XPATH, value = "/html/body/div[14]/div/header/div[2]/div/nav/ol/li[2]/a").text
    time.sleep(2)
    driver.find_element(by=By.XPATH, value="/html/body/div[14]/div/header/div[2]/div/nav/ol/li[2]/a").click()
    medicamento_1 = driver.find_element(by=By.XPATH, value="/html/body/div[9]/div/div[2]/div/div[5]/div[2]/div[2]/ul/li[1]/div/div[2]/div[1]/a[2]").text
    medicamento_2 = driver.find_element(by=By.XPATH, value="/html/body/div[9]/div/div[2]/div/div[5]/div[2]/div[2]/ul/li[1]/div/div[2]/div[3]/div/div/span/p[1]/span[2]").text
    medicamento_3 = driver.find_element(by=By.XPATH, value="/html/body/div[9]/div/div[2]/div/div[5]/div[2]/div[2]/ul/li[1]/div/div[2]/div[3]/div/div/span/p[2]/span/span[2]").text
    vida_saudavel = driver.find_element(by=By.XPATH, value="/html/body/div[9]/div/header/div[2]/div/nav/ol/li[3]/a")
    driver.find_element(by=By.XPATH, value="/html/body/div[9]/div/header/div[2]/div/nav/ol/li[3]/a").click()
    time.sleep(3)
    return {'Nome': medicamento_1, 'Preço': medicamento_2, 'Preço com desconto': medicamento_3}

if __name__ == '__main__':
    print('Static text running')
    print(main())
