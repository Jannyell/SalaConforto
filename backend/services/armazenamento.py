
import pandas as pd

from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo


# --------------------------------------
# CONFIGURAÇÕES
# --------------------------------------

FUSO_HORARIO = ZoneInfo("America/Fortaleza")

ARQUIVO = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "medicoes.csv"
)

COLUNAS = [
    "horario",
    "temperatura",
    "umidade",
    "sensacao_termica"
]


# --------------------------------------
# INICIALIZAÇÃO
# --------------------------------------

def inicializar():

    ARQUIVO.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not ARQUIVO.exists():

        pd.DataFrame(
            columns=COLUNAS
        ).to_csv(
            ARQUIVO,
            index=False
        )


# --------------------------------------
# LIMPEZA DE MEDIÇÕES ANTIGAS
# --------------------------------------

def manter_apenas_hoje():

    inicializar()

    dados = pd.read_csv(ARQUIVO)

    if dados.empty:
        return

    # Obtém a data atual de Fortaleza
    hoje = datetime.now(FUSO_HORARIO).date()

    # Converte os horários para datetime
    horarios = pd.to_datetime(
        dados["horario"],
        errors="coerce",
        utc=True
    )

    # Converte os horários para Fortaleza
    horarios = horarios.dt.tz_convert(
        "America/Fortaleza"
    )

    # Identifica quais registros pertencem ao dia atual
    dados = dados[
        horarios.dt.date == hoje
    ].copy()

    # Reescreve o CSV somente com os registros válidos
    dados.to_csv(
        ARQUIVO,
        index=False
    )


# --------------------------------------
# SALVAR MEDIÇÃO
# --------------------------------------

def salvar(medicao):

    inicializar()

    # Remove registros de dias anteriores
    manter_apenas_hoje()

    novo_registro = pd.DataFrame(
        [medicao],
        columns=COLUNAS
    )

    novo_registro.to_csv(
        ARQUIVO,
        mode="a",
        header=False,
        index=False
    )


# --------------------------------------
# LISTAR MEDIÇÕES
# --------------------------------------

def listar():

    inicializar()

    # Garante que somente os registros de hoje permaneçam
    manter_apenas_hoje()

    dados = pd.read_csv(ARQUIVO)

    return dados.to_dict(
        orient="records"
    )


# --------------------------------------
# LIMPAR TODAS AS MEDIÇÕES
# --------------------------------------

def limpar():

    inicializar()

    pd.DataFrame(
        columns=COLUNAS
    ).to_csv(
        ARQUIVO,
        index=False
    )
