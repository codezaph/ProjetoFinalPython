import tkinter as tk
import pandas as pd
import py7zr
import os
from os import path

download_path = path.join(path.expanduser('~'), 'Downloads')

class HelpersFunc:
    @staticmethod
    def input_login_gui():
        window = tk.Tk()
        window.title('Login')
        window.geometry('240x200')
        window.configure(background='white')
        window.resizable(False, False)

        # componentes
        label_email = tk.Label(window, text='Email', bg='white', fg='black')
        label_email.place(x=10, y=10)
        entry_email = tk.Entry(window, width=30, font=('Arial', 10))
        entry_email.place(x=10, y=30)
        entry_email.focus()

        label_password = tk.Label(window, text='Senha', bg='white', fg='black')
        label_password.place(x=10, y=60)
        entry_password = tk.Entry(window, width=30, show='*', font=('Arial', 10))
        entry_password.place(x=10, y=80)

        button_login = tk.Button(window, text='Login', width=25, command=window.quit, font=('Arial', 10))
        button_login.place(x=10, y=120)

        window.mainloop()

        emailData = entry_email.get().strip()
        passworData = entry_password.get()
        window.destroy()

        return emailData, passworData

        # extraindo zip

    @staticmethod
    def extract_zip(file):
        # pegar diretorio do usuario
        with py7zr.SevenZipFile(file, mode='r') as z:
            z.extractall(path=download_path)

    @staticmethod
    def convert_csv_to_excel(path):
        # Tamanho máximo por planilha
        chunk_size = 500000

        # Ler o arquivo CSV em partes menores
        reader = pd.read_csv(path, sep=';', decimal=',', chunksize=chunk_size)

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
        os.startfile(excel_file)
