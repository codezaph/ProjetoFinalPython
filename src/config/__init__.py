from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os


class Config:
    # pegar pasta downloads da maquina idenpendente do sistema operacional
    service = Service(ChromeDriverManager().install())

    # colocar o caminho para a pasta download na raiz do projeto
    prefs = {"download.default_directory": os.getcwd() + '\\downloads'}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.maximize_window()

    @staticmethod
    def get_browser():
        return Config.browser

    @staticmethod
    def get_service():
        return Config.service
