def cripto(senha):
    cod = ""

    for i in senha:
        cod = cod + chr((ord(i) + 7) % 127)
    return cod

def descripto(cod):
    senha = ""

    for i in cod:
        senha = senha + chr((ord(i) - 7) % 127)
    return senha

palavra = cripto("Estou criando um projeto sobre gerenciamento de hotéis, e preciso de alguma forma testar essa senha e esse tipo de criptografia, então, acho que é isso")

print(palavra)

assoc = descripto(palavra)

print(assoc)