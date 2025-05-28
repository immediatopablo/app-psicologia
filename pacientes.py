import streamlit as st
from helpers import carregar_dados, salvar_dados, pacientes_path

def tela_pacientes():
    st.title("Cadastro de Pacientes")
    nome = st.text_input("Nome completo")
    idade = st.number_input("Idade", min_value=0, max_value=120)
    telefone = st.text_input("Telefone")
    email = st.text_input("Email")
    endereco = st.text_input("Endereço")

    if st.button("Cadastrar"):
        if nome:
            df = carregar_dados(pacientes_path)
            novo_id = df["ID"].max() + 1 if not df.empty else 1
            usuario = st.session_state.get("usuario", "desconhecido")
            df.loc[len(df)] = [novo_id, nome, idade, telefone, email, endereco, usuario]
            salvar_dados(pacientes_path, df)
            st.success("Paciente cadastrado com sucesso!")
        else:
            st.warning("Preencha o nome do paciente.")

def listar_pacientes():
    st.title("Lista de Pacientes")
    df = carregar_dados(pacientes_path)

    # Garante que a coluna "Responsavel" exista
    if "Responsavel" not in df.columns:
        df["Responsavel"] = ""

    usuario = st.session_state.get("usuario", "")
    df = df[df["Responsavel"] == usuario]

    st.dataframe(df.reset_index(drop=True), use_container_width=True)

    if not df.empty:
        st.subheader("Editar ou Excluir Paciente")
        paciente_id = st.selectbox("Selecione o ID do paciente:", df["ID"])
        paciente_selecionado = df[df["ID"] == paciente_id].iloc[0]

        nome = st.text_input("Nome", paciente_selecionado["Nome"])
        idade = st.number_input("Idade", value=int(paciente_selecionado["Idade"]))
        telefone = st.text_input("Telefone", paciente_selecionado["Telefone"])
        email = st.text_input("Email", paciente_selecionado["Email"])
        endereco = st.text_input("Endereço", paciente_selecionado["Endereco"])

        if st.button("Atualizar Paciente"):
            df.loc[df["ID"] == paciente_id, ["Nome", "Idade", "Telefone", "Email", "Endereco"]] = [nome, idade, telefone, email, endereco]
            salvar_dados(pacientes_path, df)
            st.success("Paciente atualizado com sucesso!")

        if st.button("Excluir Paciente"):
            df = df[df["ID"] != paciente_id]
            salvar_dados(pacientes_path, df)
            st.success("Paciente excluído com sucesso!")

