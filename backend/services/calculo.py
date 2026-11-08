
def calcular_sensacao_termica(temperatura, umidade):

    # Converte temperatura de Celsius para Fahrenheit
    t = temperatura * 9 / 5 + 32

    # Umidade relativa do ar
    r = umidade

    # Estimativa inicial
    indice = 0.5 * (
        t + 61 + ((t - 68) * 1.2) + (r * 0.094)
    )

    indice = (indice + t) / 2

    # Fórmula do índice de calor
    if t >= 80 and r >= 40:
        indice = (
            -42.379
            + 2.04901523 * t
            + 10.14333127 * r
            - 0.22475541 * t * r
            - 0.00683783 * t ** 2
            - 0.05481717 * r ** 2
            + 0.00122874 * t ** 2 * r
            + 0.00085282 * t * r ** 2
            - 0.00000199 * t ** 2 * r ** 2
        )

    # Converte o resultado para Celsius
    sensacao = (indice - 32) * 5 / 9

    return round(sensacao, 1)
