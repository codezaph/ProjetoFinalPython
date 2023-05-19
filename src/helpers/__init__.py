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

    @staticmethod
    def convert_csv_to_excel(path_csv, dist_excel, filename_excel):

        chunk_size = 500000  # Tamanho máximo por planilha

        reader = pd.read_csv(path_csv, sep=',', decimal='.', chunksize=chunk_size)

        # Criar um arquivo Excel
        with pd.ExcelWriter(path.join(dist_excel, filename_excel)) as writer:
            sheet_number = 1
            for chunk in reader:
                # Salvar cada parte como uma planilha separada no arquivo Excel
                sheet_name = f'Sheet {sheet_number}'
                chunk.to_excel(writer, sheet_name=sheet_name, index=False, header=True)
                sheet_number += 1

    @staticmethod
    def extract_7z(file_path, dist_path, password=None):
        with py7zr.SevenZipFile(file_path, mode='r', password=password) as z:
            z.extractall(path=dist_path)

        # nome do arquivo extraído
        os.remove(file_path)
        return os.listdir(dist_path)[0]

    @staticmethod
    def split_csv_file(csv_path, chunk_size, dist_path):
        # Carrega o arquivo CSV em partes menores
        reader = pd.read_csv(csv_path, sep=';', decimal=',', chunksize=chunk_size)

        for i, chunk in enumerate(reader):
            print(f'Criando parte {i + 1}', end='')
            chunk.to_csv(path.join(dist_path, f"part-{i}.csv"), sep=';', decimal=',', index=False, header=True)
            print(' - OK')
