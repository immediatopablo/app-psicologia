import streamlit as st
from helpers import carregar_dados, pacientes_path, agendamentos_path, prontuarios_path

def tela_relatorios():
    st.title("Relatórios")
    pacientes = carregar_dados(pacientes_path)
    if not pacientes.empty:
        paciente_escolhido = st.selectbox("Selecione o paciente:", pacientes["Nome"])

        st.subheader("Prontuários")
        prontuarios = carregar_dados(prontuarios_path)
        prontuarios_filtrados = prontuarios[prontuarios["Paciente"] == paciente_escolhido]
        st.dataframe(prontuarios_filtrados)

        st.subheader("Agendamentos")
        agendamentos = carregar_dados(agendamentos_path)
        agendamentos_filtrados = agendamentos[agendamentos["Paciente"] == paciente_escolhido]
        st.dataframe(agendamentos_filtrados)
    else:
        st.info("Nenhum paciente cadastrado ainda.")
