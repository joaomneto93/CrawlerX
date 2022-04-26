import time
from Tela import menu
from Farmacias.Classes import Farmacia
from Funcoes.funcoes import generate_data
import os


def menu_flow(company_list: list):
    while True:
        option = menu.menu_inicial()

        if option == -1:
            time.sleep(2)
            break

        elif option is None:
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
            company_dict: dict = company_list[option]
            farmacia = Farmacia(tab_list=company_dict['tabs'], brand=company_dict['brand'],
                                old_price=company_dict['old'], wholesale=company_dict['wholesale'],
                                price1=company_dict['price'], price2=company_dict['price2'], ean=company_dict['ean'],
                                titles=company_dict['titles'], next_=company_dict['next'],
                                filename=company_dict['filename'], urls=company_dict['urls'])

            try:
                generate_data(farmacia, option)
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
