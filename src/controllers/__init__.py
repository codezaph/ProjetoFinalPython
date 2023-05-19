from selenium.webdriver.common.by import By
from time import sleep
import os

from src.config import Config
from src.helpers import HelpersFunc



DEFAULT_SLEEP_TIME = 3.5


class MainController:
    def __init__(self, email, password):
        self.email = '202202734845@alunos.estacio.br'
        self.password = 'ccff5436$'
        self.file_path = os.getcwd() + '\\downloads\\5m-Sales-Records.7z'
        self.browser = Config().get_browser()

        self._login()
        self._open_link()
        self.browser.close()

        self._convert_file()

    def _login(self):
        self.browser.get('https://estudante.estacio.br/login')
        sleep(DEFAULT_SLEEP_TIME)

        btn_enter = self.browser.find_element(By.CSS_SELECTOR,
                '#section-login > div > div > div > section > div.sc-gKRMOK > button')
        btn_enter.click()

        sleep(DEFAULT_SLEEP_TIME)

        input_email = self.browser.find_element(By.CSS_SELECTOR, '#i0116')
        input_email.send_keys(self.email)

        self.browser.find_element(By.CSS_SELECTOR, '#idSIButton9').click()

        sleep(DEFAULT_SLEEP_TIME)

        input_password = self.browser.find_element(By.CSS_SELECTOR, '#i0118')
        input_password.send_keys(self.password)
        self.browser.find_element(By.CSS_SELECTOR, '#idSIButton9').click()

        sleep(DEFAULT_SLEEP_TIME)

        # não salvar a conta
        btn_dont_save_account = self.browser.find_element(By.CSS_SELECTOR, '#idBtn_Back')
        btn_dont_save_account.click()

        sleep(DEFAULT_SLEEP_TIME + 2)

    def _open_link(self):
        self.browser.find_element(By.CSS_SELECTOR,
                                  '#card-entrega-ARA0066 > header > button').click()
        sleep(DEFAULT_SLEEP_TIME)

        self.browser.find_element(By.CSS_SELECTOR, '#segunda-tab').click()
        sleep(DEFAULT_SLEEP_TIME)

        self.browser.find_element(By.CSS_SELECTOR,
                                  '#acessar-conteudo-complementar-arquivo-64615eb275e90c00266b9ff9').click()

        # fazer o navegador esperar até o download terminar
        while True:
            if os.path.exists(self.file_path):
                break
            sleep(1)

    def _convert_file(self):
        dist_path = os.path.join(os.environ['USERPROFILE'], 'Downloads')
        name = HelpersFunc.extract_7z(self.file_path, dist_path)
        print(name)
        dist_path_file_csv = os.path.join(dist_path, name)

        chunk_size = 1000000
        HelpersFunc.split_csv_file(dist_path_file_csv, chunk_size, dist_path)

        HelpersFunc.convert_csv_to_excel(dist_path_file_csv, dist_path, filename_excel='5m Sales Records.x;lsx')

        os.remove(self.file_path)


main = MainController('email', 'senha')

