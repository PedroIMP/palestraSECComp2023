def retangulo(x, y, largura, altura):
    return (
        (x, y), (x, y + altura),
        (x + largura, y + altura), (x + largura, y),
    )

def quadrado(x, y, tamanho):
    return retangulo(x, y, tamanho, tamanho)

def perimetro(pontos):
    p = 0
    prev = pontos[-1]
    for ponto in pontos:
        x, y = ponto
        prev_x, prev_y = prev
        dist = ((x - prev_x)**2 + (y - prev_y)**2)**.5
        p += dist
        prev = ponto
    return p
