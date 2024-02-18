def cripto(senha, secret):
    cod = ""
    for i in senha:
        cod = cod + chr((ord(i) + secret) % 127)
    return cod
