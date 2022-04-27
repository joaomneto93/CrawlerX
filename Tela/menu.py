escolhas = {'1': 'DROGA RAIA', '2': 'QUALIDOC', '3': 'FARMA DELIVERY', '4': 'ULTRA FARMA', '0': 'SAIR'}

def menu_inicial():
    print('-' * 32)
    print('|' + ' ' * 30 + '|')
    print('|' + 'MENU INICIAL - CRAWLER'.center(30) + '|')
    print('|' + 'ver 1.1'.center(30) + '|')
    print('-' * 32)
    print('|' + ' ' * 30 + '|')
    print('|' + 'ESCOLHA SUA OPÇÃO:'.center(30) + '|')
    print('|' + ' ' * 30 + '|')
    print('|' + '1 - DROGA RAIA'.ljust(30) + '|')
    print('|' + '2 - QUALIDOC'.ljust(30) + '|')
    print('|' + '3 - FARMA DELIVERY'.ljust(30) + '|')
    print('|' + '4 - ULTRA FARMA'.ljust(30) + '|')
    print('|' + '0 - SAIR'.ljust(30) + '|')
    print('-' * 32)
    option = input(': ')

    if option in escolhas.keys():
        print("Opção escolhida: " + escolhas[option])
        return int(option) - 1
    else:
        return None


if __name__ == "__main__":
    menu_inicial()
