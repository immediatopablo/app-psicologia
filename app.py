import streamlit as st
from helpers import inicializar_dados, usuarios_path
from pacientes import tela_pacientes, listar_pacientes
from agendamentos import tela_agendamentos
from prontuarios import tela_prontuarios
from relatorios import tela_relatorios
import pandas as pd
import os

# Inicializa estrutura de dados
inicializar_dados()

# Autenticação
def autenticar(usuario, senha):
    usuarios = pd.read_csv(usuarios_path)
    for _, row in usuarios.iterrows():
        if row["usuario"] == usuario and row["senha"] == senha:
            return True
    return False

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    try:
        with open("data/usuario_logado.txt", "r") as f:
            usuario_salvo = f.read().strip()
            if usuario_salvo:
                st.session_state.usuario = usuario_salvo
                st.session_state.autenticado = True
    except FileNotFoundError:
        pass

if not st.session_state.autenticado:
    st.title("Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if autenticar(usuario, senha):
            st.success("Login realizado com sucesso!")
            st.session_state.autenticado = True
            st.session_state.usuario = usuario
            with open("data/usuario_logado.txt", "w") as f:
                f.write(usuario)
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")
    st.stop()

st.sidebar.markdown(f"👤 Usuário: **{st.session_state.get('usuario', 'Desconhecido')}**")
if st.sidebar.button("🔒 Logout"):
    st.session_state.autenticado = False
    if os.path.exists("data/usuario_logado.txt"):
        os.remove("data/usuario_logado.txt")
    st.rerun()

opcao = st.sidebar.selectbox("Menu", [
    "Cadastro de Pacientes", "Lista de Pacientes", "Agendamentos",
    "Prontuários", "Relatórios"
])

# Delegação por tela
if opcao == "Cadastro de Pacientes":
    tela_pacientes()
elif opcao == "Lista de Pacientes":
    listar_pacientes()
elif opcao == "Agendamentos":
    tela_agendamentos()
elif opcao == "Prontuários":
    tela_prontuarios()
elif opcao == "Relatórios":
    tela_relatorios()
