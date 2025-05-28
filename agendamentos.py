import streamlit as st
from helpers import carregar_dados, salvar_dados, pacientes_path, agendamentos_path
from datetime import datetime

def tela_agendamentos():
    st.title("Agendamentos")

    # 🧠 Pegando o usuário logado
    usuario = st.session_state.get("usuario", None)
    if not usuario:
        st.warning("Você precisa estar logado para acessar os agendamentos.")
        return

    # ✅ Carregar e filtrar pacientes do usuário
    pacientes = carregar_dados(pacientes_path)
    pacientes_usuario = pacientes[pacientes["Responsavel"] == usuario]

    if pacientes_usuario.empty:
        st.info("Nenhum paciente cadastrado por você ainda.")
        return

    nomes = pacientes_usuario["Nome"].tolist()
    paciente = st.selectbox("Paciente", nomes)
    data = st.date_input("Data")
    hora = st.time_input("Hora")

    if st.button("Agendar"):
        df = carregar_dados(agendamentos_path)

        novo_agendamento = {
            "Paciente": paciente,
            "Data": data.strftime("%Y-%m-%d"),
            "Hora": hora.strftime("%H:%M"),
            "Responsavel": usuario  # 💡 Salvar quem agendou
        }

        df.loc[len(df)] = novo_agendamento
        salvar_dados(agendamentos_path, df)
        st.success("Agendamento salvo!")

    # ✅ Mostrar apenas agendamentos do usuário
    st.subheader("Agendamentos Futuros")
    ag_df = carregar_dados(agendamentos_path)
    ag_usuario = ag_df[ag_df["Responsavel"] == usuario]

    st.dataframe(ag_usuario)

    # ✅ Excluir agendamento do próprio usuário
    if not ag_usuario.empty:
        st.subheader("Excluir Agendamento")
        ag_usuario["Index"] = ag_usuario.index
        ag_idx = st.selectbox("Selecione o índice do agendamento:", ag_usuario["Index"])
        if st.button("Excluir Agendamento"):
            ag_df = ag_df.drop(ag_idx)
            salvar_dados(agendamentos_path, ag_df.drop(columns=["Index"], errors="ignore"))
            st.success("Agendamento excluído!")
