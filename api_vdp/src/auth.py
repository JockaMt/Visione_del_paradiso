def cripto(senha, secret):
    cod = ""
    for i in senha:
        cod = cod + chr((ord(i) + secret) % 127)
    return cod

def descripto(cod, secret):
    senha = ""
    for i in cod:
        senha = senha + chr((ord(i) - secret) % 127)
    return senha
