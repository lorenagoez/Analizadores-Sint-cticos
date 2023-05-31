import input_grammar, input_strings

############################################
##############Función Closure###############
############################################
def addDot(production):
    dotProduction = production.replace("->", "->.")
    return dotProduction

def closure(I):
    J = [I]
    for i in J:
        nextsymbol = i[i.index(".") + 1]
        for k in prod:
            if k[0][0] == nextsymbol and (addDot(k)) not in J:
                J.append(addDot(k))
    return J
############################################


############################################
###Calcular LR(0) canónico (Función GoTo)###
############################################
def swap_characters(symbol, pos):
    symbol_list = list(symbol)
    temp = symbol_list[pos]
    if pos != len(symbol_list):
        symbol_list[pos] = symbol_list[pos + 1]
        symbol_list[pos + 1] = temp
        swapped = "".join(symbol_list)
        return swapped
    else:
        return "".join(symbol_list)

def goto(prod):
    nuevas_producciones = []
    pos = prod.index(".")
    if pos != len(prod) - 1:
        prod_list = list(prod)
        swapped = swap_characters(prod_list, pos)
        if swapped.index(".") != len(swapped) - 1:
            swapped_closure = closure(swapped)
            return swapped_closure
        else:
            nuevas_producciones.append(swapped)
            return nuevas_producciones
    else:
        return prod
############################################



def elements(trans, state):
    match = []
    for g in trans:
        if int(g.split()[0]) == state:
            match.append(g)
    return match

prod, initial_symbol = input_grammar.get_grammar() #Gramática desde input
closure_items = []
estados = []

print('Gramática: ')
print(prod)
prod.insert(0, "X->." + initial_symbol) #Gramática aumentada
print('\nGramática aumentada: ')
print(prod)
prod_num = {}
for i in range(1, len(prod)):
    prod_num[str(prod[i])] = i

i0 = closure("X->." + initial_symbol)
print('\nEstado inicial I0: ')
print(i0)
closure_items.append(i0)


num_estado = {}
transitions = {}
items = 0

ciclos = 0

while True:
    if len(closure_items) == 0:
        break
    print("ciclos: ", ciclos)
    ciclos += 1
    
    current_item = closure_items.pop(0)
    copy_citem = current_item
    estados.append(current_item)
    num_estado[str(current_item)] = items
    items += 1
    
    
    if len(current_item) > 1:
        for item in current_item:
            GoTo = goto(item)
            if GoTo not in closure_items and GoTo != copy_citem:
                closure_items.append(GoTo)
                transitions[str(num_estado[str(current_item)]) + " " + str(item)] = GoTo
            else:
                transitions[str(num_estado[str(current_item)]) + " " + str(item)] = GoTo

for item in estados:
    for j in range(len(item)):
        if goto(item[j]) not in estados:
            if item[j].index(".") != len(item[j]) - 1:
                estados.append(goto(item[j]))

print("\nEstados: ", len(estados))
for i in range(len(estados)):
    print(i, ":", estados[i])


rules = {}
for i in range(len(estados)):
    if i in rules:
        continue
    else:
        transition_list = elements(transitions, i)
        trans_dic = {}
        for j in transition_list:
            rhs = j.split()[1].split('->')[1]
            dot_next = rhs[rhs.index('.') + 1]
            trans_dic[dot_next] = num_estado[str(transitions[j])]

        if trans_dic != {}:
            rules[i] = trans_dic
            
print('\nReglas GoTo:')
for key, value in rules.items():
    for inner_key, inner_value in value.items():
        print(f'GoTo({key},{inner_key}): estado', inner_value)




#################################################################
print('\nCalcular tabla de análisis sintáctico\n')
#################################################################
table = []
terminales = sorted(list(input_grammar.terminales(prod)))
no_terminales = sorted(list(input_grammar.no_terminales(prod)))
table.append([''] + terminales + no_terminales)

table_dic = {}

for i in range(len(estados)):
    actions = [''] * (len(terminales) + len(no_terminales))
    trans_dic = {}
    # Shift, Reduce, Accept
    try:
        #Añade shift
        for j in rules[i]:
            if j.isupper() == False and j != '' and j != '.':
                ind = terminales.index(j)
                actions[ind] = 'S' + str(rules[i][j])
                trans_dic[terminales[ind]] = 'S' + str(rules[i][j])

    except Exception:
        #Añade reduce
        if i != 1:
            dot_prod = list(estados[i][0])
            dot_prod.remove('.')
            dot_prod = "".join(dot_prod)
            transition_list = [i] + ['r' + str(prod_num[dot_prod])] * len(terminales)
            transition_list += [''] * len(no_terminales)
            table.append(transition_list)
            for j in terminales:
                trans_dic[j] = 'r' + str(prod_num[dot_prod])
        else:
            #Estado de aceptación
            transition_list = [i] + [''] * (len(terminales) + len(no_terminales))
            transition_list[-1] = 'Accept'
            table.append(transition_list)

    try:
        #Añade GoTo
        for j in rules[i]:
            if j.isupper():
                ind = no_terminales.index(j)
                actions[len(terminales) + ind] = rules[i][j]

                trans_dic[j] = str(rules[i][j])

        table.append([i] + actions)
    except Exception:
        pass

    if trans_dic == {}:
        table_dic[i] = {'$': 'Accept'}
    else:
        table_dic[i] = trans_dic
######################################################################

print(table_dic)


def parse_string(string):
    stack = [0]
    i = 0    #Índice actual en la cadena
    accepted = False
    
    while True:
        try:
            try:
                prods = rules[stack[-1]]
                prod_i = prods[string[i]]
            except Exception:
                prod_i = None
            
            #Action
            try:
                tab = table_dic[stack[-1]]
                tab_i = tab[string[i]]  
            except Exception:
                tab = table_dic[stack[-2]]
                tab_i = tab[stack[-1]]  

            ##Accept##
            if tab_i == 'Accept':
                accepted = True
                break
            ##Accept##
            else:
                if tab_i[0] == 'S' and not str(stack[-1]).isupper():
                    stack.append(string[i])
                    stack.append(prod_i)
                    i += 1
                elif tab_i[0] == 'r':
                    x = None
                    
                    for j in prod_num:
                        if prod_num[j] == int(tab_i[1]):
                            x = j
                            break

                    length = 2 * (len(x.split('->')[1]))

                    for _ in range(length):
                        stack.pop()
                    stack.append(x[0])
                else:
                    stack.append(int(tab_i))
        except Exception:
            accepted = False
            break

    if accepted:
        return "La cadena '" + string.replace('$', '') + "' es válida."
    else:
        return "La cadena '" + string.replace('$', '') + "' no es válida"

strings = input_strings.input_strings()
for string in strings:
    result = parse_string(string)
    print(result)
