import requests
import random
import time

# Endereço da API Flask
URL_API = "http://127.0.0.1:5000/api/leituras"

# Intervalo entre as medições:
INTERVALO = 20


def gerar_leitura():
    return {
        "temperatura": round(random.uniform(24, 34), 1),
        "umidade": round(random.uniform(40, 85), 1)
    }

def enviar_leitura(dados):

    try:
        resposta = requests.post(
            URL_API,
            json=dados,
            timeout=5
        )

        resposta.raise_for_status()

        print("Leitura enviada com sucesso!")
        print(f"Temperatura: {dados['temperatura']} °C")
        print(f"Umidade: {dados['umidade']} %")
        print("-" * 35)

    except requests.exceptions.RequestException as erro:
        print(f"Erro ao enviar leitura: {erro}")

def iniciar_simulador():

    print("Simulador SalaConforto iniciado!")
    print("Pressione CTRL + C para encerrar.")
    print("-" * 35)

    try:
        while True:

            dados = gerar_leitura()

            enviar_leitura(dados)

            time.sleep(INTERVALO)

    except KeyboardInterrupt:
        print("\nSimulador encerrado.")


if __name__ == "__main__":
    iniciar_simulador()