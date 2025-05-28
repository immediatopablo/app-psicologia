import streamlit as st
import pandas as pd
import os
import json
from helpers import inicializar_dados, usuarios_path
from pacientes import tela_pacientes, listar_pacientes
from agendamentos import tela_agendamentos
from prontuarios import tela_prontuarios
from relatorios import tela_relatorios

# 📌 Configuração de personalização
config_path = "data/config.json"

def carregar_config():
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def salvar_config(config):
    with open(config_path, "w") as f:
        json.dump(config, f)

# 🔹 Inicializa estrutura de dados
inicializar_dados()

# ✅ Aplica estilo fixo na tela de login SEM CAIXA BRANCA
st.markdown("""
    <style>
        .stApp {
            background-color: #E6E6FA; /* Roxo claro fixo */
        }
        .stButton>button {
            background-color: #6A5ACD; /* Roxo médio */
            color: white;
            font-size: 16px;
            border-radius: 12px;
            padding: 10px 20px;
            border: none;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #483D8B; /* Roxo escuro ao passar o mouse */
        }
        .stTextInput>div>div>input {
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #ccc;
        }
        .login-container {
            text-align: center;
            padding: 10px;
            max-width: 400px;
            margin: auto;
            margin-top: 30px;
        }
    </style>
    """, unsafe_allow_html=True)

# 🧠 Explicação sobre o sistema
st.markdown("""
# 🧠 Sistema para Psicólogos
Bem-vindo ao seu sistema de gestão de prontuários, consultas e pacientes!  
Acompanhe históricos de atendimento, organize sua agenda e tenha informações acessíveis de forma rápida e segura.
""")

# 🔐 Autenticação
def autenticar(usuario, senha):
    usuarios = pd.read_csv(usuarios_path)
    return any((usuarios["usuario"] == usuario) & (usuarios["senha"] == senha))

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.subheader("🔑 Login no Sistema")
    
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
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# 🎨 Carrega preferências do usuário após login
usuario = st.session_state.get("usuario", None)
config = carregar_config()
cor_fundo = config.get(usuario, {}).get("cor_fundo", "#FFFFFF")

# ✅ Aplica estilo personalizado após login
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {cor_fundo};
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# 📌 Barra lateral de personalização
st.sidebar.markdown(f"👤 Usuário: **{usuario}**")
if st.sidebar.button("🔒 Logout"):
    st.session_state.autenticado = False
    if os.path.exists("data/usuario_logado.txt"):
        os.remove("data/usuario_logado.txt")
    st.rerun()

st.sidebar.subheader("Personalizar Sistema 🎨")
nova_cor = st.sidebar.color_picker("Escolha sua cor preferida", cor_fundo)

if st.sidebar.button("Salvar Preferências"):
    config[usuario] = {"cor_fundo": nova_cor}
    salvar_config(config)
    st.success("Personalização salva! Recarregue a página para ver as mudanças.")

# 🎯 Menu de navegação
opcao = st.sidebar.selectbox("Menu", [
    "Cadastro de Pacientes", "Lista de Pacientes", "Agendamentos",
    "Prontuários", "Relatórios"
])

# 🔄 Direciona o usuário para cada funcionalidade
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
