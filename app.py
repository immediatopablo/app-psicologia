import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Caminho dos usuários (pode adaptar se estiver em outra pasta)
usuarios_path = "data/usuarios.csv"

# Função de verificação
def autenticar(usuario, senha):
    usuarios = pd.read_csv(usuarios_path)
    for _, row in usuarios.iterrows():
        if row["usuario"] == usuario and row["senha"] == senha:
            return True
    return False

# Sessão de autenticação
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# 🔄 Verifica se já há um login salvo em arquivo
if not st.session_state.autenticado:
    try:
        with open("data/usuario_logado.txt", "r") as f:
            usuario_salvo = f.read().strip()
            if usuario_salvo:
                st.session_state.usuario = usuario_salvo
                st.session_state.autenticado = True
    except FileNotFoundError:
        pass

# Tela de login
if not st.session_state.autenticado:
    st.title("Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if autenticar(usuario, senha):
            st.success("Login realizado com sucesso!")
            st.session_state.autenticado = True
            st.session_state.usuario = usuario

            # ✅ Salva o login em arquivo
            os.makedirs("data", exist_ok=True)
            with open("data/usuario_logado.txt", "w") as f:
                f.write(usuario)

            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")

    st.stop()

# ⬇️ Botão de logout na sidebar
if st.session_state.get("autenticado", False):
    st.sidebar.markdown(f"👤 Usuário: **{st.session_state.get('usuario', 'Desconhecido')}**")
    if st.sidebar.button("🔒 Logout"):
        st.session_state.autenticado = False
        st.session_state.usuario = ""

        # 🧹 Remove o arquivo de login
        if os.path.exists("data/usuario_logado.txt"):
            os.remove("data/usuario_logado.txt")

        st.rerun()

# Criação de diretório de dados
if not os.path.exists("data"):
    os.makedirs("data")

# Arquivos CSV simulando banco de dados
pacientes_path = "data/pacientes.csv"
agendamentos_path = "data/agendamentos.csv"
prontuarios_path = "data/prontuarios.csv"

# Inicializar arquivos se não existirem
for path, cols in [
    (pacientes_path, ["ID", "Nome", "Idade", "Telefone", "Email", "Endereco"]),
    (agendamentos_path, ["Paciente", "Data", "Hora"]),
    (prontuarios_path, ["Paciente", "Data", "Anotação"])
]:
    if not os.path.exists(path):
        pd.DataFrame(columns=cols).to_csv(path, index=False)

# Funções auxiliares
def carregar_dados(caminho):
    return pd.read_csv(caminho)

def salvar_dados(caminho, df):
    df.to_csv(caminho, index=False)

# Sidebar
st.sidebar.title("Menu")
opcao = st.sidebar.selectbox("Escolha uma opção:", [
    "Cadastro de Pacientes", "Lista de Pacientes", "Agendamentos",
    "Prontuários", "Relatórios"
])

# Cadastro de Pacientes
if opcao == "Cadastro de Pacientes":
    st.title("Cadastro de Pacientes")
    nome = st.text_input("Nome completo")
    idade = st.number_input("Idade", min_value=0, max_value=120)
    telefone = st.text_input("Telefone")
    email = st.text_input("Email")
    endereco = st.text_input("Endereço")

    if st.button("Cadastrar"):
        if nome:
            df = carregar_dados(pacientes_path)
            novo_id = len(df) + 1
            df.loc[len(df)] = [novo_id, nome, idade, telefone, email, endereco]
            salvar_dados(pacientes_path, df)
            st.success("Paciente cadastrado com sucesso!")
        else:
            st.warning("Preencha o nome do paciente.")

# Lista de Pacientes
elif opcao == "Lista de Pacientes":
    st.title("Lista de Pacientes")
    df = carregar_dados(pacientes_path)
    st.dataframe(df)

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

# Agendamentos
elif opcao == "Agendamentos":
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

# Prontuários
elif opcao == "Prontuários":
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

# Relatórios
elif opcao == "Relatórios":
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