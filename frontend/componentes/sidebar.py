import streamlit as st

def renderizar_sidebar():
    """
    Renderiza a sidebar e retorna o limite da sensação térmica desejado.
    """

    st.sidebar.title("Configurações")
    
    st.sidebar.subheader("Limites de conforto")

    # Limite de sensação térmica
    limite_sensacao_maximo= st.sidebar.number_input(
            "Sensação térmica (°C)",
            min_value=0.0,
            max_value=60.0,
            value=30.0,
            step=0.5
        )
    

    return limite_sensacao_maximo