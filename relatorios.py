import streamlit as st
from helpers import carregar_dados, pacientes_path, agendamentos_path, prontuarios_path

def tela_relatorios():
    st.title("Relatórios")

    # Verifica se o usuário está logado
    usuario = st.session_state.get("usuario", None)
    if not usuario:
        st.warning("Você precisa estar logado para acessar os relatórios.")
        return

    # Carrega apenas os pacientes cadastrados pelo usuário
    pacientes = carregar_dados(pacientes_path)
    pacientes_usuario = pacientes[pacientes["Responsavel"] == usuario]

    if not pacientes_usuario.empty:
        paciente_escolhido = st.selectbox("Selecione o paciente:", pacientes_usuario["Nome"])

        st.subheader("Prontuários")
        prontuarios = carregar_dados(prontuarios_path)
        prontuarios_filtrados = prontuarios[
            (prontuarios["Paciente"] == paciente_escolhido) &
            (prontuarios["Responsavel"] == usuario)
        ]
        st.dataframe(prontuarios_filtrados.drop(columns=["Responsavel"], errors="ignore"))

        st.subheader("Agendamentos")
        agendamentos = carregar_dados(agendamentos_path)
        agendamentos_filtrados = agendamentos[
            (agendamentos["Paciente"] == paciente_escolhido) &
            (agendamentos["Responsavel"] == usuario)
        ]
        st.dataframe(agendamentos_filtrados.drop(columns=["Responsavel"], errors="ignore"))
    else:
        st.info("Nenhum paciente cadastrado por você ainda.")
