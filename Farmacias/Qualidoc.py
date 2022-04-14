import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from scrapy import Selector

class Qualidoc():

    def __init__(self):
        self.url = "https://www.qualidoc.com.br/"

    def generate_data(self):
        print("Não implementado até o momento")