from selenium.webdriver.common.by import By
from time import sleep
import os

from src.config import Config
from src.helpers import HelpersFunc

DEFAULT_SLEEP_TIME = 5


class MainController:
    def __init__(self, email, password):
        self.email = email
        self.password = password
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
                                              '#section-login > div > div > div > section > div > button')
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
        download_path_project = os.getcwd() + '\\downloads'
        parts_path = os.path.join(download_path_project, 'parts')

        # criar a pasta 'parts' se ela não existir
        if not os.path.exists(parts_path):
            os.mkdir(parts_path)

        name = HelpersFunc.extract_7z(self.file_path, download_path_project)

        # separar o arquivo .csv em partes menores
        chunk_size = 1000000

        print('--' * 20)
        print('Separando o arquivo em partes menores...\n')

        file_csv_path = os.path.join(download_path_project, name)
        HelpersFunc.split_csv_file(file_csv_path, chunk_size, parts_path)

        # removendo o arquivo .csv baixado
        os.remove(file_csv_path)

        # converter as partes para .csv
        download_path_sys = os.path.join(os.environ['USERPROFILE'], 'Downloads')

        print('\n')
        print('--' * 20)
        print('\nConvertendo as partes para .xlsx...\n')

        # pegar caminho de cada parte
        parts = os.listdir(parts_path)

        total_parts = len(parts)
        for i, part in enumerate(parts):
            print(f'{i + 1}/{total_parts}', end='')
            path_part = os.path.join(parts_path, part)
            HelpersFunc.convert_csv_to_excel(
                path_part, download_path_sys, f'5m Sales Records-{part.replace(".csv", ".xlsx")}')

            os.remove(path_part)
            print(' - OK')

            if i == 0:
                break

        os.rmdir(parts_path)
        os.rmdir(download_path_project)

        # abrir pasta
        os.startfile(download_path_sys)
