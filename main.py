from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from time import sleep
from selenium.webdriver.common.by import By
from os import path
import py7zr
import math

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')


def split_csv_file(csv_file, chunk_size, output_folder):
    # Carrega o arquivo CSV em partes menores
    df = pd.read_csv(csv_file, sep=';', decimal=',', chunksize=chunk_size)

    # Divide o arquivo em partes menores
    chunk_number = 1
    for chunk in df:
        # Salva cada parte em um arquivo CSV separado
        chunk.to_csv(f"{output_folder}/part_{chunk_number}.csv", index=False, sep=';', decimal=',')
        chunk_number += 1

# fazer download na pasta certa
def abreLink(link, caminhoDownload):
    # seta o local do download
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': path.expanduser(caminhoDownload)}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)

    # abre o link da estacio
    driver.get(link)
    sleep(5)

    # navega até o lugar do download
    entrar = driver.find_element(By.XPATH, value="/html/body/div[1]/section/div/div/div/section/div[1]/button").click()
    sleep(5)

    colocaEmail = driver.find_element(By.XPATH,
                                      value="/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[2]/div[2]/div/input[1]").send_keys(
        '202202705772@alunos.estacio.br')
    sleep(3)

    avanco = driver.find_element(By.XPATH,
                                 value="/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[4]/div/div/div/div[2]/input").click()
    sleep(5)

    colocaSenha = driver.find_element(By.XPATH,
                                      value='/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div/div[2]/input').send_keys(
        '!Zaph1234')
    sleep(3)

    login = driver.find_element(By.XPATH,
                                value='/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[4]/div[2]/div/div/div/div/input').click()
    sleep(2)

    clicaNao = driver.find_element(By.XPATH,
                                   value='/html/body/div/form/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div[1]/input').click()
    sleep(10)

    entraAulaPython = driver.find_element(By.XPATH,
                                          value='/html/body/div[1]/main/section/article/section[1]/section/div[2]/div/div/section[5]/div[1]/button').click()
    sleep(5)

    conteudoComplementar = driver.find_element(By.XPATH, value='/html/body/div[1]/main/section/aside/section/section[2]/div[1]/button[2]').click()
    sleep(5)

    download = driver.find_element(By.XPATH,
                                   value='/html/body/div[1]/main/section/aside/section/section[2]/div[3]/section[1]/section/div[3]/div[2]/div/section/div/div[1]/button').click()
    sleep(30)

    driver.quit()


# extraindo zip
def extrair_arquivo_7z(arquivo_7z, destino):
    with py7zr.SevenZipFile(arquivo_7z, mode='r') as z:
        z.extractall(path=r"C:\Users\Code\Downloads")


sleep(15)
# Convertendo Csv para Excel
def convertCsvToExcel(caminhoCsv):
    chunk_size = 500000  # Tamanho máximo por planilha

    # Ler o arquivo CSV em partes menores
    reader = pd.read_csv(caminhoCsv, sep=';', decimal=',', chunksize=chunk_size)

    excel_file = "C:/Users/Code/Downloads/5m Sales Records.xlsx"

    # Criar um arquivo Excel
    with pd.ExcelWriter(excel_file) as writer:
        sheet_number = 1
        for chunk in reader:
            # Salvar cada parte como uma planilha separada no arquivo Excel
            sheet_name = f"Sheet {sheet_number}"
            chunk.to_excel(writer, sheet_name=sheet_name, index=False, header=True)
            sheet_number += 1

    print("Arquivo Excel gerado com sucesso!")


###############################
#INICIO DO PROGRAMA
###############################

# URL do link de download
url = 'https://estudante.estacio.br/login'
# Pasta onde o arquivo será baixado
arquivoBaixado = r"C:/Users/Code/Downloads"

# Faz o download do arquivo
abreLink(url, arquivoBaixado)

# Aguarde o download ser concluído
sleep(30)

# Caminho completo do arquivo baixado
caminhoArquivoBaixado = path.join(arquivoBaixado, '5m-Sales-Records.7z')

# Extrai o arquivo baixado
extrair_arquivo_7z(caminhoArquivoBaixado, arquivoBaixado)

# Define o caminho do arquivo CSV
caminhoCsv = r"C:/Users/Code/Downloads/5m Sales Records.csv"


tamanho_parte = 1000000
# Define a pasta de saída para as partes divididas
pasta_saida = r"C:/Users/Code/Downloads"


# Divide o arquivo CSV em partes menores
split_csv_file(caminhoCsv, tamanho_parte, pasta_saida)


# Converte o arquivo CSV para Excel
convertCsvToExcel(arquivoBaixado)


