def input_strings():
    strings = []
    print("Ingrese las cadenas que desea analizar: ")
    while True:
        string = input()
        if not string:
            break
        string += "$"
        strings.append(string) 
    return strings