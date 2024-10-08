txt = open("separadas.txt", "r")
symbolos = []

for line in txt:
    symbolos.append(line[:len(line)-1])

triangulos = []

for first_symbol in symbolos:
    fs_fc = first_symbol.split()[0]
    fs_sc = first_symbol.split()[1]
    for second_symbol in symbolos:
        ss_fc = second_symbol.split()[0]
        ss_sc = second_symbol.split()[1]
        if ss_sc == fs_sc and fs_fc !=ss_fc :
            triangulos.append([first_symbol, second_symbol, ""])

triangulos_ok = []

for triangulo in triangulos:
    final_symbol = f"{triangulo[1].split()[0]} {triangulo[0].split()[0]}"
    if final_symbol in symbolos:
        triangulo[0] = triangulo[0].replace(" ", "")
        triangulo[1] = triangulo[1].replace(" ", "")
        triangulo[2] = final_symbol.replace(" ", "")
        triangulos_ok.append(triangulo)

print(triangulos_ok)
