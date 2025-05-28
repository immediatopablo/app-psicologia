import streamlit as st
from datetime import datetime
import pandas as pd
from helpers import carregar_dados, salvar_dados, pacientes_path, prontuarios_path

def tela_prontuarios():
    st.title("Prontuários")

    # 🧠 Recupera o usuário logado
    usuario = st.session_state.get("usuario", None)
    if not usuario:
        st.warning("Você precisa estar logado para acessar os prontuários.")
        return

    # ✅ Carrega e filtra pacientes vinculados ao usuário
    pacientes = carregar_dados(pacientes_path)
    pacientes_usuario = pacientes[pacientes["Responsavel"] == usuario]

    if pacientes_usuario.empty:
        st.info("Nenhum paciente cadastrado por você ainda.")
        return

    nomes = pacientes_usuario["Nome"].tolist()
    paciente = st.selectbox("Paciente", nomes)
    anotacao = st.text_area("Anotação do Atendimento")

    if st.button("Salvar Prontuário"):
        df = carregar_dados(prontuarios_path)
        data_hoje = datetime.now().strftime("%Y-%m-%d")

        novo_prontuario = {
            "Paciente": paciente,
            "Data": data_hoje,
            "Anotação": anotacao,
            "Responsavel": usuario
        }

        # 🚀 Correção: Adicionando corretamente ao DataFrame
        df = pd.concat([df, pd.DataFrame([novo_prontuario])], ignore_index=True)

        salvar_dados(prontuarios_path, df)
        st.success("Prontuário salvo com sucesso!")

    # ✅ Exibe somente prontuários do usuário
    pront_df = carregar_dados(prontuarios_path)
    pront_usuario = pront_df[pront_df["Responsavel"] == usuario]

    if not pront_usuario.empty:
        st.subheader("Excluir Prontuário")
        pront_usuario["Index"] = pront_usuario.index
        pront_idx = st.selectbox("Selecione o índice do prontuário:", pront_usuario["Index"])
        if st.button("Excluir Prontuário"):
            pront_df = pront_df.drop(pront_idx)
            salvar_dados(prontuarios_path, pront_df.drop(columns=["Index"], errors="ignore"))
            st.success("Prontuário excluído!")

        st.subheader("Prontuários Recentes")
        st.dataframe(pront_usuario.drop(columns=["Responsavel"]))
    else:
        st.info("Nenhum prontuário encontrado para os seus pacientes.")
