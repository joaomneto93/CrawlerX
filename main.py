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
    time.sleep(10)
    element = driver.find_element(by=By.XPATH, value="/html/body/div[13]/div/div[2]/div/div[3]/div[6]/div[3]/div[2]/div[2]")
    return element


if __name__ == '__main__':
    print('Static text running')
    print(main())
