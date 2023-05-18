from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class Config:
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)
    browser.maximize_window()

    @staticmethod
    def get_browser():
        return Config.browser

    @staticmethod
    def get_service():
        return Config.service
