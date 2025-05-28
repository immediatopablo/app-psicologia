import streamlit as st
from helpers import carregar_dados, salvar_dados, pacientes_path, agendamentos_path
from datetime import datetime

def tela_agendamentos():
    st.title("Agendamentos")
    pacientes = carregar_dados(pacientes_path)
    nomes = pacientes["Nome"].tolist()

    paciente = st.selectbox("Paciente", nomes)
    data = st.date_input("Data")
    hora = st.time_input("Hora")

    if st.button("Agendar"):
        df = carregar_dados(agendamentos_path)
        df.loc[len(df)] = [paciente, data.strftime("%Y-%m-%d"), hora.strftime("%H:%M")]
        salvar_dados(agendamentos_path, df)
        st.success("Agendamento salvo!")

    st.subheader("Agendamentos Futuros")
    ag_df = carregar_dados(agendamentos_path)
    st.dataframe(ag_df)

    if not ag_df.empty:
        st.subheader("Excluir Agendamento")
        ag_df["Index"] = ag_df.index
        ag_idx = st.selectbox("Selecione o índice do agendamento:", ag_df["Index"])
        if st.button("Excluir Agendamento"):
            ag_df = ag_df.drop(ag_idx)
            salvar_dados(agendamentos_path, ag_df.drop(columns=["Index"]))
            st.success("Agendamento excluído!")
