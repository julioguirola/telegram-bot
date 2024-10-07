txt = open("separadas.txt", "r")
monedas = []
symbolos = []

for line in txt:
    symbolos.append(line[:len(line)-1])
    par = line.split()
    for moneda in par:
        if moneda not in monedas:
            monedas.append(moneda)

triangulos = []

for coin in monedas:
    for par in symbolos:
        if coin == par.split()[0]:
            for par2 in symbolos:
                if par.split()[0] == par2.split()[1] and par.split()[1] != par2.split()[0]:
                    triangulos.append([par.replace(" ",""),f"{par.split()[1]} {par2.split()[0]}",par2.replace(" ","")])

triangulos_ok = []


for triangulo in triangulos:
    for sym in symbolos:
        if triangulo[1] == sym:
            triangulos_ok.append([triangulo[0], sym.replace(" ", ""), triangulo[2]])


print(triangulos_ok)
