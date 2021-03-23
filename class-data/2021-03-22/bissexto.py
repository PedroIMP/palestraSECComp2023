# Se o ano é divisível por 400, então é bissexto.
# Senão, se é divisível por 100, não é bissexto.
# Senão, se é divisível por 4, é bissexto.

def ano_eh_bisexto(ano):
    if ano % 400 == 0:
        return True
    elif ano % 100 == 0:
        return False
    elif ano % 4 == 0:
        return True
    else:
        return False


def ano_eh_bisexto_2(ano):
    if ano % 400 == 0:
        return True
    elif ano % 100 != 0 and ano % 4 == 0:
        return True
    else:
        return False


def ano_eh_bisexto_3(ano):
    if ano % 400 == 0 or (ano % 100 != 0 and ano % 4 == 0):
        return True
    else:
        return False


def ano_eh_bisexto_4(ano):
    return ano % 400 == 0 or (ano % 100 != 0 and ano % 4 == 0)


ano = input('Entre com o ano: ')

# Converter ano para int
ano = int(ano)

if ano_eh_bisexto_4(ano):
    print('Fevereiro terá 29 dias em', ano)
else:
    print('Fevereiro terá 28 dias em', ano)