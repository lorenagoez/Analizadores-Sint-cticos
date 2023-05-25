def recursionIzquierda(diccionario):
  # Guarda las nuevas reglas
  reglas = {}

  for lhs in diccionario:
    alpha = []  #Se almacenan las reglas con recursión izquierda
    beta = []  #Se almacenan las reglas sin recursión izquierda

    todosrhs = diccionario[lhs]
    for subrhs in todosrhs:
      if subrhs[0] == lhs:
        alpha.append(subrhs[1:])
      else:
        beta.append(subrhs)

    if len(alpha) != 0:

      # Genera símbolo único '
      lhs_ = lhs + "'"
      while (lhs_ in diccionario.keys()) \
        or (lhs_ in reglas.keys()):
        lhs_ += "'"

      #Genera los beta
      for b in range(0, len(beta)):
        beta[b].append(lhs_)
      diccionario[lhs] = beta

      #Genera los alfa
      for a in range(0, len(alpha)):
        alpha[a].append(lhs_)
      alpha.append(['#'])
      reglas[lhs_] = alpha

  #Se guardan las nuevas reglas
  for izquierda in reglas:
    diccionario[izquierda] = reglas[izquierda]
  return diccionario

def first(regla):
  global reglas, noTerminales, terminalesUsr, diccionario, firsts

  # Verifica si el primer símbolo es terminal o epsilon
  if len(regla) != 0 and (regla is not None):
    if regla[0] in terminalesUsr:
      return regla[0]
    elif regla[0] == '#':
      return '#'

  # Condición para los no terminales
  if len(regla) != 0:
    if regla[0] in list(diccionario.keys()):
      # fres temporary list of result
      fres = []
      reglashRhs = diccionario[regla[0]]

      # Se llama al first de cada regla
      for itr in reglashRhs:
        indivRes = first(itr)
        if indivRes is not None:
          if type(indivRes) is list:
            fres.extend(indivRes)
          else:
            fres.append(indivRes)

      # En caso de no haber un epsilon
      if '#' not in fres:
        return fres
      else:
        nuevaLista = []
        fres.remove('#')
        if len(regla) > 1:
          nuevaRespuesta = first(regla[1:])
          if nuevaRespuesta is not None:
            if type(nuevaRespuesta) is list:
              nuevaLista = fres + nuevaRespuesta
            else:
              nuevaLista = fres + [nuevaRespuesta]
          else:
            nuevaLista = fres
          return nuevaLista
        fres.append('#')
        return fres

  # Si no se encuentra en el diccionario, devuelve una lista vacía
  return []


def follow(noTerminalFollow, visited=None):
  global simboloInicial, reglas, noTerminales, terminalesUsr, diccionario, firsts, follows

  if visited is None:
    visited = set()

  # Verifica si el no terminal ya ha sido visitado
  if noTerminalFollow in visited:
    return None

  # Añade el no terminal a los visitados
  visited.add(noTerminalFollow)

  # Para el símbolo inicial retorna "$"
  solucion = set()
  if noTerminalFollow == simboloInicial:
    solucion.add('$')

  # Recorre todas las reglas
  for actualnoTerminal in diccionario:
    rhs = diccionario[actualnoTerminal]

    # Recorre todas las producciones de no terminales
    for subregla in rhs:
      if noTerminalFollow in subregla:
        while noTerminalFollow in subregla:
          indexnoTerminal = subregla.index(noTerminalFollow)
          subregla = subregla[indexnoTerminal + 1:]

          # Verifica si hay más símbolos en la subregla
          if len(subregla) != 0:
            res = first(subregla)

            # Por si se encuentra un epsilon
            if '#' in res:
              nuevaLista = []
              res.remove('#')
              nuevaRes = follow(actualnoTerminal, visited)
              if nuevaRes != None:
                if type(nuevaRes) is list:
                  nuevaLista = res + nuevaRes
                else:
                  nuevaLista = res + [nuevaRes]
              else:
                nuevaLista = res
              res = nuevaLista
            else:
              res = None  # Asegurarse de que res sea None si no hay más símbolos en la subregla
          else:
            if noTerminalFollow != actualnoTerminal:
              res = follow(actualnoTerminal, visited)
            else:
              res = None  # Asegurarse de que res sea None si la subregla se reduce a epsilon

          # Almacenar el follow
          if res is not None:
            if type(res) is list:
              for g in res:
                solucion.add(g)
            else:
              solucion.add(res)

  follows[noTerminalFollow] = solucion
  return list(solucion)



def calcularFirst():
  global reglas, noTerminales, \
   terminalesUsr, diccionario, firsts
  for regla in reglas:
    k = regla.split("->")

    #Se remueven espacios innecesarios
    k[0] = k[0].strip()
    k[1] = k[1].strip()
    rhs = k[1]
    multirhs = rhs.split('|')
    for i in range(len(multirhs)):
      multirhs[i] = multirhs[i].strip()
      multirhs[i] = multirhs[i].split()
    diccionario[k[0]] = multirhs

  diccionario = recursionIzquierda(diccionario)

  #Calcula el first de cada regla
  for y in list(diccionario.keys()):
    t = set()
    for sub in diccionario.get(y):
      res = first(sub)
      if res != None:
        if type(res) is list:
          for u in res:
            t.add(u)
        else:
          t.add(res)

    #Se guardan los resultados
    firsts[y] = t


def calcularFollows():
  global simboloInicial, reglas, noTerminales,\
   terminalesUsr, diccionario, firsts, follows
  for NT in diccionario:
    conjuntoSolucion = set()
    solucion = follow(NT)
    if solucion is not None:
      for g in solucion:
        conjuntoSolucion.add(g)
    follows[NT] = conjuntoSolucion


def crearTabla():
  import copy
  global diccionario, firsts, follows, terminalesUsr

  maxFirst = 0
  maxFollow = 0
  for u in diccionario:
    k1 = len(str(firsts[u]))
    k2 = len(str(follows[u]))
    if k1 > maxFirst:
      maxFirst = k1
    if k2 > maxFollow:
      maxFollow = k2

  #Se crea una matriz y una lista de no terminales
  listanoTerminales = list(diccionario.keys())
  terminales = copy.deepcopy(terminalesUsr)
  terminales.append('$')

  #Estado vacío inicial
  matriz = []
  for x in diccionario:
    fila = []
    for y in terminales:
      fila.append('')
    # of $ append one more col
    matriz.append(fila)
  confirmacionLL = True  #Clasifica la gramática

  #Implementación de las reglas
  for lhs in diccionario:
    rhs = diccionario[lhs]
    for y in rhs:
      res = first(y)
      #Para cuando se encuentre un epsilon
      if '#' in res:
        if type(res) == str:
          firstFollow = []
          opcion = follows[lhs]
          if opcion is str:
            firstFollow.append(opcion)
          else:
            for u in opcion:
              firstFollow.append(u)
          res = firstFollow
        else:
          res.remove('#')
          res = list(res) +\
           list(follows[lhs])
      ttemp = []  #Se añaden las reglas a la tabla
      if type(res) is str:
        ttemp.append(res)
        res = copy.deepcopy(ttemp)
      for c in res:
        xnt = listanoTerminales.index(lhs)
        yt = terminales.index(c)
        if matriz[xnt][yt] == '':
          matriz[xnt][yt] = matriz[xnt][yt] \
             + f"{lhs}->{' '.join(y)}"
        else:
          #Si la regla ya está
          if f"{lhs}->{y}" in matriz[xnt][yt]:
            continue
          else:
            confirmacionLL = False
            matriz[xnt][yt] = matriz[xnt][yt] \
               + f",{lhs}->{' '.join(y)}"

  if confirmacionLL:
    print("\nLa gramática es LL(1).\n")

  return (matriz, confirmacionLL, terminales)


def analizarCadena(tabla, gramatica, listaTabla, cadena, terminales,
                   simboloInicial):

  #Más de una entrada en una celda de la tabla
  if gramatica == False:
    mensaje = "La gramática no es LL(1)"
    return mensaje

  #Stack bucffer
  stack = [simboloInicial, '$']
  buffer = []
  cadena = cadena.split()
  cadena.reverse()
  buffer = ['$'] + cadena

  while True:
    #Terminar loop si ya todos los símbolos están asignados
    if stack == ['$'] and buffer == ['$']:
      return "La cadena es válida!"
    elif stack[0] not in terminales:
      x = list(diccionario.keys()).index(stack[0])
      y = listaTabla.index(buffer[-1])
      if tabla[x][y] != '':
        entrada = tabla[x][y]
        lhs_rhs = entrada.split("->")
        lhs_rhs[1] = lhs_rhs[1].replace('#', '').strip()
        entradaRhs = lhs_rhs[1].split()
        stack = entradaRhs + stack[1:]
      else:
        return "La cadena es inválida."
    else:
      if stack[0] == buffer[-1]:
        buffer = buffer[:-1]
        stack = stack[1:]
      else:
        return "La cadena es inválida."


print("LL1 PARSER")
print("Ingrese una gramática libre de contexto: ")

reglas = []

while True:
  entrada = input()
  if entrada == '':
    break
  reglas.append(entrada)

noTerminales = []  #Se almacenan los no terminales

for i in range(1, len(reglas)):
  if reglas[i][0].isupper():
    print("printeando...")
    print(reglas[i][0])
    noTerminales.append(reglas[i][0])

terminalesUsr = []  #Se almacenan los terminales

for regla in reglas:
  for char in regla:
    if char.islower() or char.isdigit():
      if not char in terminalesUsr:
        terminalesUsr.append(char)
    elif char.isupper() and char not in noTerminales and char != "S":
      if not char in terminalesUsr:
        terminalesUsr.append(char)

cadenaInput = input("Ingrese una cadena para ser analizada: ")

diccionario = {}
firsts = {}
follows = {}
calcularFirst()
simboloInicial = list(diccionario.keys())[0]
calcularFollows()
(tablaParseo, resultado, termino) = crearTabla()

if cadenaInput != None:
  validez = analizarCadena(tablaParseo, resultado, termino, cadenaInput,
                           terminalesUsr, simboloInicial)
  print(validez)
else:
  print("\nNo hay cadena para analizar")
