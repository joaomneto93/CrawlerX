import time
from Tela import menu


def menu_flow(class_list: dict):
    while True:
        opcao = menu.menu_inicial()

        if opcao == '0':
            time.sleep(2)
            break

        elif opcao is None:
            print("Opção não existente, tente novamente")
            time.sleep(2)

        else:
            farmacia = class_list[opcao]
            farmacia.generate_data()
            time.sleep(2)


# if __name__ == '__main__':
#     menu_flow({'DROGA RAIA': })
