import sys

def get_grammar():
    productions = []
    print("Ingrese su gramática:")
    production = input().replace(" ", "")
    if not production:
        print("Error: Debe ingresar al menos una producción.")
        sys.exit()
    initial_symbol = production.split('->')[0].strip()
    right_side = production.split('->')[1].split('|')
    productions.extend([production.replace(production.split('->')[1], rs) for rs in right_side])

    while True:
        production = input().replace(" ", "")
        if not production:
            break
        if '->' in production:
            right_side = production.split('->')[1].split('|')
            productions.extend([production.replace(production.split('->')[1], rs) for rs in right_side])
        else:
            productions.extend([p.replace('->', production) for p in productions[-len(right_side):]])

    return productions, initial_symbol

def terminales(G):
    terminales = set()   #Al ser conjunto no se agregan carácteres repetidos
    for i in G:
        char = i.split('->')
        for j in char[1].strip():
            if j.isupper() == False and j != '.' and j != '':
                terminales.add(j)

    terminales.add('$')
    return terminales

def no_terminales(G):
    nterminales = set()  #Al ser conjunto no se agregan carácteres repetidos
    for i in G:
        char = i.split('->')
        for j in char[1].strip():
            if j.isupper():
                nterminales.add(j)
    return nterminales