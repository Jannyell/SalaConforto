import streamlit as st
import requests
import pandas as pd


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

st.title("🌡️ SalaConforto")
st.caption(
    "Sistema de monitoramento de temperatura, "
    "umidade e sensação térmica"
)

st.divider()


# --------------------------------------
# CONFIGURAÇÃO DO LIMITE
# --------------------------------------

st.subheader("Configuração de conforto térmico")

limite = st.number_input(
    "Defina o limite máximo de sensação térmica (°C):",
    min_value=0.0,
    max_value=60.0,
    value=30.0,
    step=0.5
)

st.divider()


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

    df["horario"] = pd.to_datetime(
        df["horario"],
        errors="coerce",
        utc=True
    )

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

    coluna1, coluna2, coluna3 = st.columns(3)

    with coluna1:

        st.metric(
            "🌡️ Temperatura",
            f"{ultima['temperatura']:.1f} °C"
        )

    with coluna2:

        st.metric(
            "💧 Umidade",
            f"{ultima['umidade']:.1f}%"
        )

    with coluna3:

        st.metric(
            "🔥 Sensação térmica",
            f"{ultima['sensacao_termica']:.1f} °C"
        )

    # --------------------------------------
    # ALERTA DE SENSAÇÃO TÉRMICA
    # --------------------------------------

    if ultima["sensacao_termica"] >= limite:

        st.error(
            f"⚠️ Atenção! A sensação térmica está em "
            f"{ultima['sensacao_termica']:.1f} °C, "
            f"atingindo ou ultrapassando o limite "
            f"de {limite:.1f} °C."
        )

    else:

        st.success(
            f"✅ Sensação térmica dentro do limite definido "
            f"({limite:.1f} °C)."
        )

    st.divider()

    # --------------------------------------
    # GRÁFICOS
    # --------------------------------------

    st.subheader("Histórico das medições")

    grafico1, grafico2 = st.columns(2)

    with grafico1:

        st.markdown("**🌡️ Temperatura**")

        grafico_temperatura = (
            df.set_index("horario")[["temperatura"]]
        )

        st.line_chart(grafico_temperatura)

    with grafico2:

        st.markdown("**💧 Umidade**")

        grafico_umidade = (
            df.set_index("horario")[["umidade"]]
        )

        st.line_chart(grafico_umidade)

    st.markdown("**🔥 Sensação térmica**")

    grafico_sensacao = (
        df.set_index("horario")[["sensacao_termica"]]
    )

    st.line_chart(grafico_sensacao)

    st.divider()

    # --------------------------------------
    # HISTÓRICO COMPLETO
    # --------------------------------------

    st.subheader("Histórico de medições")

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
        hide_index=True
    )


# --------------------------------------
# EXECUÇÃO
# --------------------------------------

atualizar_painel()
