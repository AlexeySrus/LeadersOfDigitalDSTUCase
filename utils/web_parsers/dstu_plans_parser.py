import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class DSTUPlansParser(object):
    def __init__(self):
        firefox_options = Options()
        firefox_options.add_argument('--headless')
        firefox_options.add_argument('--start-maximized')
        self.driver = webdriver.Firefox(
            firefox_options=firefox_options,
            executable_path='data/geckodriver'
        )
        self.main_page = 'https://edu.donstu.ru/Plans/'

    def __call__(self, ):
        self.driver.get(self.main_page)
