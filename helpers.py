import os
import pandas as pd

DATA_DIR = "data"
usuarios_path = os.path.join(DATA_DIR, "usuarios.csv")
pacientes_path = os.path.join(DATA_DIR, "pacientes.csv")
agendamentos_path = os.path.join(DATA_DIR, "agendamentos.csv")
prontuarios_path = os.path.join(DATA_DIR, "prontuarios.csv")

def carregar_dados(caminho):
    return pd.read_csv(caminho)

def salvar_dados(caminho, df):
    df.to_csv(caminho, index=False)

def inicializar_dados():
    os.makedirs(DATA_DIR, exist_ok=True)
    arquivos = [
        (pacientes_path, ["ID", "Nome", "Idade", "Telefone", "Email", "Endereco"]),
        (agendamentos_path, ["Paciente", "Data", "Hora"]),
        (prontuarios_path, ["Paciente", "Data", "Anotação"]),
    ]
    for caminho, colunas in arquivos:
        if not os.path.exists(caminho):
            pd.DataFrame(columns=colunas).to_csv(caminho, index=False)
