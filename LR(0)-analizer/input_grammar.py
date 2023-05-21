import sys

def get_grammar():
    productions = []
    print("Ingrese su gramática:")
    production = input()
    if not production:
        print("Error: Debe ingresar al menos una producción.")
        sys.exit()
    initial_symbol = production.split('->')[0].strip()
    productions.append(production)

    while True:
        production = input()
        if not production:
            break
        productions.append(production)
    
    return productions, initial_symbol