def cripto(senha):
    cod = ""

    for i in senha:
        cod = cod + chr(ord(i) + 7)
    return cod

def descripto (cod):
    senha = ""

    for i in cod:
        senha = senha + chr(ord(i) - 7)
    return senha

palavra = cripto("eu tenho depressao")

print(palavra)

assoc = descripto(palavra)

print(assoc)