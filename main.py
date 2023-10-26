#
# Explorando a biblioteca / framework streamlit
# Autor: Arnott Ramos Caiado
#
# Projeto: calendário
# data: 26/10/2023
#
import streamlit as st
import pandas as pd


opcoes =("Opção 1","Opção 2", "Opção 3")
st.markdown("# Calendario")
st.title("Titulo")
st.header("Cabeçalho")
st.subheader("Subcabeçalho")
st.selectbox("Escolha", opcoes)
st.button("Enviar")

