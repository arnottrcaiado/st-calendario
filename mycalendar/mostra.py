import streamlit as st

colors = {
    "inicio": "#ADD8E6",
    "teorico": "#00BFFF",
    "complementar": "#87CEFA",
    "teorica_final": "#0000FF",
    "pratico": "#0000CD",
    "recesso": "#836FFF",
    "fds": "#B0C4DE",
    "feriado": "#C0C0C0",
    "ferias": "#A9A9A9"
}

def generate_table(data):
    table_data = []
    header = ["Ano", "Mês", "Calendário"]
    table_data.append(header)
    
    for entry in data:
        split_data = entry.split(';')
        month = split_data[0]
        year = split_data[1]
        teoricas_praticas = split_data[2:-3]
        teoricas = split_data[-3]
        praticas = split_data[-2]
        total = split_data[-1]
        
        calendar_representation = generate_calendar_representation(teoricas_praticas)
        
        row = [year, month, calendar_representation]
        table_data.append(row)

    return table_data

def generate_calendar_representation(teoricas_praticas):
    representation = ""
    
    for day in teoricas_praticas:
        day_completo = day
        aula_type = day.split('-')[2]
        day_number = day.split('-')[0]
        day_week = day.split('-')[1]
        representation += f"{day_week}({day_number}) "

    return representation

def generate_colored_box(color_code):
    return f'<div style="display: inline-block; width: 20px; height: 20px; background-color: {color_code};"></div>'

def generate_calendar(
        agencia, curso, turma, turno, municipio,
        formacaoTeorica, chtotal, chteoricatotal, chDiaria,
        formacaoInicial, formacaoFinal, periodoFerias, inicioeTermino, data,
        logo_path="https://github.com/arnottrcaiado/st-calendario/blob/master/mycalendar/static/ciee.jpg"
    ):
    st.title("Calendário de Aulas")
    
    col1, col2 = st.columns(2)

    with col1:
        st.image(logo_path, use_column_width=True)

    with col2:
        st.header("Cronograma - Calendário")
        st.write(f"Agência: {agencia} | Curso: {curso} | Turma: {turma} | Turno: {turno} | Município: {municipio}")
        st.write(f"Formação Teórica: {formacaoTeorica} | Carga Horária Total: {chtotal} h | C.H. Teórica: {chteoricatotal} h | C.H. Diária: {chDiaria} h")
        st.write(f"Formação Inicial: {formacaoInicial} | Formação Final: {formacaoFinal}")
        st.write(f"Férias: {periodoFerias}")
        st.write(f"Início e Término do Contrato: {inicioeTermino}")

    st.table(generate_table(data))

    st.header("Legenda")
    legenda = [
        ("inicio", "i Formação Inicial"),
        ("teorico", "t,T Aulas Teóricas CIEE"),
        ("complementar", "c Aulas Teóricas Complementares (c) CIEE"),
        ("teorica_final", "f Formação final"),
        ("pratico", "p Atividades Práticas na Empresa"),
        ("recesso", "r Atividades Práticas na Empresa - Recesso no CIEE"),
        ("fds", "x Finais de Semanas"),
        ("feriado", "X Feriados"),
        ("ferias", "F Férias")
    ]

    for color_class, description in legenda:
        color = colors.get(color_class, "#FFFFFF")
        st.markdown(f"{generate_colored_box(color)} = {description}", unsafe_allow_html=True)

