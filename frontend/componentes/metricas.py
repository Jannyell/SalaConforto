import streamlit as st


def verificar_limite_sensacao(sensacao_termica, limite):
    """
    Verifica se a sensação térmica atingiu ou ultrapassou o limite.
    """

    return sensacao_termica <= limite


def renderizar_metricas(ultima, limite):
    """
    Renderiza as três métricas principais da dashboard.
    """

    coluna1, coluna2, coluna3 = st.columns(3)

    dentro_limite = verificar_limite_sensacao(ultima['temperatura'], limite)

    # TEMPERATURA
    with coluna1:

        with st.container(border=True):

            st.metric(
                "🌡️ Temperatura",
                f"{ultima['temperatura']:.1f} °C"
            )

            # Espaço reservado para manter o alinhamento
            st.markdown(
                "<div style='height: 45px'></div>",
                unsafe_allow_html=True
            )

    # UMIDADE
    with coluna2:

        with st.container(border=True):

            st.metric(
                "💧 Umidade",
                f"{ultima['umidade']:.1f}%"
            )

            st.markdown(
                "<div style='height: 45px'></div>",
                unsafe_allow_html=True
            )

    # SENSAÇÃO TÉRMICA
    with coluna3:

        with st.container(border=True):

            st.metric(
                "🔥 Sensação térmica",
                f"{ultima['sensacao_termica']:.1f} °C"
            )

            dentro_limite = verificar_limite_sensacao(ultima['sensacao_termica'], limite)

            if dentro_limite:

                cor_fundo = "#d1fae5"
                cor_texto = "#065f46"
                mensagem = f"✓ Dentro do limite: {limite:.1f} °C"

            else:

                cor_fundo = "#fee2e2"
                cor_texto = "#991b1b"
                mensagem = f"⚠ Acima do limite: {limite:.1f} °C"

            st.markdown(
                f"""
                <div style="
                    height: 40px;
                    display: flex;
                    align-items: center;
                ">
                    <span style="
                        background-color: {cor_fundo};
                        color: {cor_texto};
                        padding: 6px 10px;
                        border-radius: 8px;
                        font-size: 12px;
                        font-weight: 600;
                        white-space: nowrap;
                    ">
                        {mensagem}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )