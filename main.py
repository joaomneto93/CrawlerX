from Tela.menu_flow import menu_flow
from Farmacias.Raia import DrogaRaia
from Farmacias.Qualidoc import Qualidoc
from Farmacias.FarmaDelivery import FarmaDelivery
from Farmacias.UltraFarma import UltraFarma

lista_farmacias = {'1': DrogaRaia, '2': Qualidoc, '3': FarmaDelivery, '4': UltraFarma}

if __name__ == '__main__':
    print('Scrapper running')
    menu_flow(lista_farmacias)
