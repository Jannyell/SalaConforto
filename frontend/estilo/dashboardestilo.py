import streamlit as st


# ESTILIZAÇÃO DA DASHBOARD
def carregar_estilo():
    st.markdown("""
            <style>

            /* Remove o espaço excessivo no topo */
            .block-container {
                padding-top: 0.5rem;
                padding-bottom: 2rem;
            }

            /* Ajusta o espaçamento dos títulos */
            h1 {
                margin-top: 0rem;
                padding-top: 0rem;
            }

            h2, h3 {
                margin-top: 0.5rem;
            }

            /* Ajusta o espaço entre título e descrição */
            [data-testid="stHeading"] {
                gap: 0.2rem;
            }

            /* Remove o fundo visual do cabeçalho */
            [data-testid="stHeader"] {
                background: transparent;
            }

            /* Ajusta o espaçamento dos elementos */
            .element-container {
                margin-bottom: 0.3rem;
            }

            </style>
            """, unsafe_allow_html=True)
