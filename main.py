# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# import time
# from scrapy import Selector
# import requests
# import pandas as pd
from Tela.menu_flow import menu_flow
from Farmacias.Raia import DrogaRaia
from Farmacias.Qualidoc import Qualidoc

lista_farmacias = {'1': DrogaRaia(), '2': Qualidoc()}

if __name__ == '__main__':
    print('Scrapper running')
    menu_flow(lista_farmacias)
