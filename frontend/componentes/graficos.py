import streamlit as st


def renderizar_graficos(df):

    st.subheader("Histórico das medições")

    grafico1, grafico2, grafico3 = st.columns(3)

    with grafico1:
        st.markdown("**🌡️ Temperatura**")

        grafico_temperatura = df.set_index("horario")[["temperatura"]]

        st.line_chart(
            grafico_temperatura,
            color="#E75480"
        )

    with grafico2:
        st.markdown("**💧 Umidade**")

        grafico_umidade = df.set_index("horario")[["umidade"]]

        st.line_chart(
            grafico_umidade,
            color="#3498DB"
        )

    with grafico3:
        st.markdown("**🔥 Sensação térmica**")

        grafico_sensacao = df.set_index("horario")[["sensacao_termica"]]

        st.line_chart(
            grafico_sensacao,
            color="#F39C45"
        )

    st.divider()