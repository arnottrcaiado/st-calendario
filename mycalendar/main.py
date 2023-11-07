#
# Explorando a biblioteca / framework streamlit
# Autor: Arnott Ramos Caiado
#
# Projeto: calendário
# data: 26/10/2023
#

import streamlit as st
import mostra as ms
import calcula as ca
from mostra import generate_calendar
import pandas as pd


# Substitua 'tabelaAgencias' pelos valores reais que você deseja usar para o seletor.
tabelaAgencias = [  "RECIFE",
                    "OLINDA",
                    "IPOJUCA",
                    "FACULDADE DOS GUARARAPES",
                    "FAFIRE",
                    "LIMOEIRO",
                    "GRAVATÁ",
                    "SALGUEIRO",
                    "CARPINA",
                    "VITÓRIA",
                    "GARANHUNS",
                    "SERRA TALHADA",
                    "CARUARU",
                    "PETROLINA",
                    "UCN - SÃO PAULO",
                    "UCN - ESPÍRITO SANTO",
                    "UCN - RIO GRANDE DO SUL",
                    "UCN - PARANÁ",
                    "UCN - RIO DE JANEIRO",
                    "UCN - MINAS GERAIS",
                    "UCN - SANTA CATARINA",
                    "CARPINAR" ]


# Função para mostrar a tabela quando o botão for clicado
def mostrarMunicipios(dados):
    st.write(dados)

# Função para fazer upload e atualizar a tabela
def atualizar_tabela():
    uploaded_file = st.file_uploader("Carregar arquivo CSV para atualizar a tabela", type=["csv"])
    if uploaded_file is not None:
        uploaded_data = pd.read_csv(uploaded_file)
        data = uploaded_data
        return data


# Configurações gerais da página
st.set_page_config(
    page_title="Calendário - Tela de Entrada de Dados [v30.8.2023]",
    page_icon="📅",
    layout="centered",
)

# Título da página
st.title("Calendário - Tela de Entrada")

# Criando um contêiner para alinhar o formulário
with st.container():
    tabelaFeriados = pd.read_csv("./dados/feriados.csv") #path folder of the data file
    tabelamunicipios = pd.read_csv("./dados/municipiosPe.csv")
    # Botão para mostrar a tabela
    if st.button('Municipios'):
       st.write(tabelamunicipios)
    if st.button('Feriados'):
       st.write(tabelaFeriados)


    # Formulário
    st.subheader("Dados de Entrada")
    agencia = st.selectbox("Agência:", tabelaAgencias)
    curso = st.text_input("Curso:", "")
    turma = st.text_input("Turma:", "")
    turno = st.radio("Turno:", ["Manhã", "Tarde", "Manhã e Tarde"])
    municipio = st.text_input("Município:", "")
    data_ini = st.date_input("Data de Início:")
    ferias_inicio = st.date_input("Férias (início):")
    ferias_final = st.date_input("Férias (final):")
    carga_horaria_total = st.number_input("Carga Horária Total:", min_value=0, max_value=3000)
    carga_horaria_teorica = st.number_input("Carga Horária Teórica:", min_value=0, max_value=1000)
    formacao_inicial = st.number_input("Formação Inicial (CH):", min_value=0, max_value=200)
    horas_semana = st.number_input("Horas Teóricas por Semana:", min_value=0, max_value=10)
    dia_semana = st.radio("Aulas Fixas:", ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"])
    semana_complementar = st.radio("Aulas Complementares (semana):", ["Sem Aulas Complementares", "Primeira", "Segunda", "Terceira", "Quarta"])
    dia_complementar = st.radio("Aulas Complementares:", ["Sem Aulas Complementares", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"])

    # Botões
    col1, col2, col3 = st.columns(3)
    if col1.button("Calendário (1)"):
        # Lógica para processar Calendário (1)
        st.write("Você pressionou o botão Calendário (1)")
          # Testar a função generate_calendar com valores de amostra.
        sample_data = ["Janeiro;2023;1-S-i;2-M-i;3-T-t;4-W-t;5-T-t;25;5;30"]
        generate_calendar("Agencia1", "Curso1", "Turma1", "Turno1", "Municipio1", "FormacaoTeorica1", 100, 50, 5, "FormacaoInicial1", "FormacaoFinal1", "PeriodoFerias1", "InicioeTermino1", sample_data)


    if col2.button("Calendário (2)"):
        # Lógica para processar Calendário (2)
        st.write("Você pressionou o botão Calendário (2)")

    if col3.button("Download xls"):
        # Lógica para processar Download xls
        st.write("Você pressionou o botão Download xls")

# Resultado
st.markdown("---")
st.subheader("Resultado:")
# Lógica para exibir o resultado

# Estilos CSS
st.markdown(
    """
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 450px;
            margin: 0 auto;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 8px;
            background-color: #fff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
        }
        .stContainer {
            padding: 0 20px 20px 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
