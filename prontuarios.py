import streamlit as st
from datetime import datetime
from helpers import carregar_dados, salvar_dados, pacientes_path, prontuarios_path

def tela_prontuarios():
    st.title("Prontuários")
    pacientes = carregar_dados(pacientes_path)
    nomes = pacientes["Nome"].tolist()

    paciente = st.selectbox("Paciente", nomes)
    anotacao = st.text_area("Anotação do Atendimento")

    if st.button("Salvar Prontuário"):
        df = carregar_dados(prontuarios_path)
        data_hoje = datetime.now().strftime("%Y-%m-%d")
        df.loc[len(df)] = [paciente, data_hoje, anotacao]
        salvar_dados(prontuarios_path, df)
        st.success("Prontuário salvo com sucesso!")

    pront_df = carregar_dados(prontuarios_path)
    st.subheader("Excluir Prontuário")
    pront_df["Index"] = pront_df.index
    pront_idx = st.selectbox("Selecione o índice do prontuário:", pront_df["Index"])
    if st.button("Excluir Prontuário"):
        pront_df = pront_df.drop(pront_idx)
        salvar_dados(prontuarios_path, pront_df.drop(columns=["Index"]))
        st.success("Prontuário excluído!")
