import pandas as pd
from pathlib import Path


# --------------------------------------
# CAMINHO DO ARQUIVO CSV
# --------------------------------------

ARQUIVO_CSV = (
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

    # Garante que a pasta data exista
    ARQUIVO_CSV.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Cria o CSV caso não exista
    if not ARQUIVO_CSV.exists():

        pd.DataFrame(
            columns=COLUNAS
        ).to_csv(
            ARQUIVO_CSV,
            index=False
        )


# --------------------------------------
# SALVAR MEDIÇÃO
# --------------------------------------

def salvar(medicao):

    inicializar()

    dados = pd.DataFrame(
        [medicao],
        columns=COLUNAS
    )

    dados.to_csv(
        ARQUIVO_CSV,
        mode="a",
        header=False,
        index=False
    )


# --------------------------------------
# LISTAR MEDIÇÕES
# --------------------------------------

def listar():

    inicializar()

    dados = pd.read_csv(ARQUIVO_CSV)

    # Garante a presença das colunas esperadas
    dados = dados.reindex(columns=COLUNAS)

    # Substitui valores ausentes por None
    dados = dados.astype(object).where(
        pd.notna(dados),
        None
    )

    return dados.to_dict(
        orient="records"
    )


# --------------------------------------
# LIMPAR HISTÓRICO
# --------------------------------------

def limpar():

    inicializar()

    dados = pd.DataFrame(
        columns=COLUNAS
    )

    dados.to_csv(
        ARQUIVO_CSV,
        index=False
    )