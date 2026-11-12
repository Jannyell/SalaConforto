import streamlit as st
import requests
import pandas as pd

from componentes.sidebar import renderizar_sidebar
from componentes.metricas import renderizar_metricas
from componentes.graficos import renderizar_graficos

from estilo.dashboardestilo import carregar_estilo


# --------------------------------------
# CONFIGURAÇÕES DA INTERFACE
# --------------------------------------

st.set_page_config(
    page_title="SalaConforto",
    page_icon="🌡️",
    layout="wide"
)

URL_API = "http://127.0.0.1:5000/api/leituras"


# --------------------------------------
# TÍTULO
# --------------------------------------

st.title("SalaConforto")
st.caption(
    "Sistema de monitoramento de temperatura, "
    "umidade e sensação térmica"
)

# --------------------------------------
# CARREGAR ESTILO DA DASHBOARD
# --------------------------------------

carregar_estilo()

# --------------------------------------
# CONFIGURAÇÃO DO LIMITE
# --------------------------------------

limite = renderizar_sidebar()

# --------------------------------------
# PAINEL DE MONITORAMENTO
# --------------------------------------

@st.fragment(run_every="5s")
def atualizar_painel():

    try:
        resposta = requests.get(
            URL_API,
            timeout=3
        )

        resposta.raise_for_status()

        leituras = resposta.json()

    except requests.exceptions.RequestException as erro:

        st.error(
            f"Não foi possível conectar ao servidor Flask: {erro}"
        )
        return

    except ValueError:

        st.error("O servidor Flask retornou uma resposta inválida.")

        return

    # --------------------------------------
    # VERIFICAÇÃO DOS DADOS RECEBIDOS
    # --------------------------------------

    if isinstance(leituras, dict):

        # Aceita também uma resposta no formato {"leituras": [...]}
        leituras = leituras.get("leituras", [])

    if not isinstance(leituras, list):

        st.error(
            "Formato de dados inesperado. "
            "A API precisa retornar uma lista de leituras."
        )
        return

    if not leituras:

        st.info("Aguardando as primeiras medições...")
        return

    # --------------------------------------
    # ORGANIZAÇÃO DOS DADOS
    # --------------------------------------

    df = pd.DataFrame(leituras)

    colunas_obrigatorias = [
        "horario",
        "temperatura",
        "umidade",
        "sensacao_termica"
    ]

    # Verifica se todas as colunas existem
    colunas_ausentes = [
        coluna
        for coluna in colunas_obrigatorias
        if coluna not in df.columns
    ]

    if colunas_ausentes:

        st.error(
            "A API não retornou todos os campos necessários: "
            + ", ".join(colunas_ausentes)
        )

        st.write("Dados recebidos da API:")
        st.json(leituras)

        return

    # --------------------------------------
    # TRATAMENTO DOS DADOS
    # --------------------------------------

    
# --------------------------------------
# TRATAMENTO DOS DADOS
# --------------------------------------

    # Converte os horários para UTC
    df["horario"] = pd.to_datetime(
        df["horario"],
        errors="coerce",
        utc=True
    )

    # Converte para o horário de Fortaleza
    df["horario"] = df["horario"].dt.tz_convert(
        "America/Fortaleza"
    )

    # Converte as colunas numéricas
    colunas_numericas = [
        "temperatura",
        "umidade",
        "sensacao_termica"
    ]

    for coluna in colunas_numericas:
        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce"
        )

    # Remove registros inválidos
    df = df.dropna(
        subset=colunas_obrigatorias
    )

    if df.empty:
        st.warning(
            "Não existem medições válidas disponíveis."
        )
        return

    # Ordena as medições pelo horário
    df = df.sort_values("horario")

    # --------------------------------------
    # ÚLTIMA MEDIÇÃO
    # --------------------------------------

    ultima = df.iloc[-1]

    # --------------------------------------
    # INDICADORES PRINCIPAIS
    # --------------------------------------
    
    renderizar_metricas(ultima, limite)

    # --------------------------------------
    # GRÁFICOS
    # --------------------------------------

    renderizar_graficos(df)

    # --------------------------------------
    # HISTÓRICO COMPLETO
    # --------------------------------------

    st.subheader("Registros do ambiente")

    df_exibicao = df.sort_values(
        "horario",
        ascending=False
    ).copy()

    # Converte para horário local na exibição
    df_exibicao["horario"] = (
        df_exibicao["horario"]
        .dt.tz_convert("America/Fortaleza")
        .dt.strftime("%d/%m/%Y %H:%M:%S")
    )

    st.dataframe(
        df_exibicao,
        use_container_width=True,
        hide_index=True,
        height=150
    )

# --------------------------------------
# EXECUÇÃO
# --------------------------------------

atualizar_painel()

