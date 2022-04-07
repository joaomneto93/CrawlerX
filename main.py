import time
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.service import Service


def get_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument('disable-dev-shm-usage')
    options.add_argument("no-sandbox")

    driver = Chrome(service=Service("chromedriver_win32/chromedriver.exe"), options=options)
    driver.get(url=url)
    return driver

class DrogaRaia:
    def __init__(self):
        self.driver = None
        self.url = "https://www.drogaraia.com.br/"
