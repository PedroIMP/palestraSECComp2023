# Este programa lê um número natural n e calcula
# a soma dos valores 0, 1, 2, ..., n - 1

def soma(n):
    i = 0
    s = 0
    
    while i < n:
        s = s + i
        i = i + 1
    
    return s

limite = int(input('n: '))
while limite != 0: 
    resultado = soma(limite)
    print('A soma de 0 até', limite - 1, 'é', resultado)
    limite = int(input('outro n: '))

print('Tchau')