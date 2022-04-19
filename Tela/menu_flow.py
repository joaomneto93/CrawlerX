import time
from Tela import menu
from Funcoes.funcoes import generate_data
import os


def menu_flow(class_list: dict):
    while True:
        opcao = menu.menu_inicial()

        if opcao == '0':
            time.sleep(2)
            break

        elif opcao is None:
            print("Opção não existente, tente novamente")
            time.sleep(0.75)
            print('.')
            time.sleep(0.75)
            print('.')
            time.sleep(0.75)
            print('.')
            time.sleep(0.75)
            os.system('cls')

        else:
            farmacia = class_list[opcao]
            try:
                generate_data(farmacia)
            except AttributeError:
                print("Opção não implementada até o momento!")
            time.sleep(0.75)
            print('.')
            time.sleep(0.75)
            print('.')
            time.sleep(0.75)
            print('.')
            time.sleep(0.75)
            os.system('cls')