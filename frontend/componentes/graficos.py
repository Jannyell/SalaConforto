import streamlit as st
import altair as alt


# --------------------------------------
# FUNÇÃO PARA CRIAR OS GRÁFICOS
# --------------------------------------

def criar_grafico(df, coluna, cor, nome):

    # Seleciona o ponto mais próximo do mouse
    selecao = alt.selection_point(
        nearest=True,
        on="pointerover",
        fields=["horario"],
        empty=False
    )

    base = alt.Chart(df).encode(
        x=alt.X(
            "horario:T",
            axis=alt.Axis(
                format="%H:%M",
                title=None,
                labelAngle=0,
                tickCount=5
            )
        )
    )

    # Linha principal
    linha = base.mark_line(
        color=cor,
        strokeWidth=2.5
    ).encode(
        y=alt.Y(
            f"{coluna}:Q",
            title=None
        )
    )

    # Pontos invisíveis que detectam a posição do mouse
    seletores = base.mark_point(
        opacity=0
    ).add_params(
        selecao
    )

    # Ponto destacado ao passar o mouse
    pontos = base.mark_point(
        color=cor,
        size=90,
        filled=True
    ).encode(
        y=f"{coluna}:Q",
        opacity=alt.condition(
            selecao,
            alt.value(1),
            alt.value(0)
        ),
        tooltip=[
            alt.Tooltip(
                "horario:T",
                title="Horário",
                format="%H:%M"
            ),
            alt.Tooltip(
                f"{coluna}:Q",
                title=nome,
                format=".1f"
            )
        ]
    )

    # Linha vertical indicando o horário selecionado
    regra = base.mark_rule(
        color="gray",
        strokeDash=[4, 4]
    ).encode(
        opacity=alt.condition(
            selecao,
            alt.value(0.7),
            alt.value(0)
        )
    ).transform_filter(
        selecao
    )

    # Combina todos os elementos
    grafico = alt.layer(
        linha,
        seletores,
        regra,
        pontos
    ).properties(
        height=300
    )

    return grafico


# --------------------------------------
# GRÁFICOS DA DASHBOARD
# --------------------------------------

def renderizar_graficos(df):

    st.subheader("Histórico das medições")

    df_graficos = df.copy()

    df_graficos["horario"] = (
        df_graficos["horario"]
        .dt.tz_convert("America/Fortaleza")
    )

    grafico1, grafico2, grafico3 = st.columns(3)

    with grafico1:

        st.markdown("**🌡️ Temperatura**")

        grafico = criar_grafico(
            df_graficos,
            "temperatura",
            "#E75480",
            "Temperatura (°C)"
        )

        st.altair_chart(
            grafico,
            use_container_width=True
        )

    with grafico2:

        st.markdown("**💧 Umidade**")

        grafico = criar_grafico(
            df_graficos,
            "umidade",
            "#3498DB",
            "Umidade (%)"
        )

        st.altair_chart(
            grafico,
            use_container_width=True
        )

    with grafico3:

        st.markdown("**🔥 Sensação térmica**")

        grafico = criar_grafico(
            df_graficos,
            "sensacao_termica",
            "#F39C45",
            "Sensação térmica (°C)"
        )

        st.altair_chart(
            grafico,
            use_container_width=True
        )

    st.divider()
