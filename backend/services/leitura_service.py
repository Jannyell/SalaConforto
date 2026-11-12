
import math
from datetime import datetime
from zoneinfo import ZoneInfo

from services import armazenamento
from services import calculo


def registrar_leitura(dados):

    # Verifica se os dados recebidos são um dicionário
    if not isinstance(dados, dict):
        return {"erro": "Dados inválidos"}, 400

    temperatura = dados.get("temperatura")
    umidade = dados.get("umidade")

    # Converte os valores para números
    try:
        temperatura = float(temperatura)
        umidade = float(umidade)

    except (ValueError, TypeError):
        return {"erro": "Valores numéricos são obrigatórios"}, 400

    # Verifica se os valores são válidos
    if not math.isfinite(temperatura) or not math.isfinite(umidade):
        return {"erro": "Valores numéricos inválidos"}, 400

    if not 0 <= umidade <= 100:
        return {"erro": "Umidade inválida"}, 400

    # Calcula a sensação térmica
    sensacao = calculo.calcular_sensacao_termica(
        temperatura,
        umidade
    )

    # Monta a leitura
    leitura = {
        "horario": datetime.now(ZoneInfo("America/Fortaleza")).isoformat(timespec="seconds"),
        "temperatura": temperatura,
        "umidade": umidade,
        "sensacao_termica": sensacao
    }

    # Salva no CSV
    armazenamento.salvar(leitura)

    return {
        "mensagem": "Leitura registrada",
        "dados": leitura
    }, 201


def obter_ultima_leitura():

    leituras = armazenamento.listar()

    if not leituras:
        return {"mensagem": "Nenhuma leitura disponível"}, 404

    return leituras[-1], 200


def listar_leituras():

    return armazenamento.listar(), 200
