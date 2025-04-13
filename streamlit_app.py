import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from io import BytesIO

# ---- Configuração da página ----
st.set_page_config(page_title="Uploader de Planilhas", page_icon="📈", layout="centered")

# ---- Conexão com PostgreSQL (Railway) ----
DATABASE_URL = "postgresql://postgres:vFqfjqGKjbzNaSscGyLjvWifXrhaifHy@ballast.proxy.rlwy.net:10605/railway"
engine = create_engine(DATABASE_URL)

# ---- Autenticação simples ----
senha_correta = "admin123"
st.markdown("## 🔐 Login")

senha = st.text_input("Digite a senha de acesso", type="password")

if senha != senha_correta:
    st.warning("Acesso restrito. Informe a senha correta.")
    st.stop()

# ---- Interface principal após login ----
st.markdown("## 📁 Upload de Planilhas")
uploaded_files = st.file_uploader(
    "Selecione uma ou mais planilhas Excel (.xlsx)",
    type=["xlsx"],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            # Lê o Excel
            df = pd.read_excel(BytesIO(uploaded_file.read()))

            # Nome da tabela baseado no nome do arquivo
            nome_tabela = uploaded_file.name.split(".")[0].replace("Tb|", "").lower()

            # Envia para o banco (replace = substitui se já existir)
            df.to_sql(nome_tabela, engine, if_exists="replace", index=False)

            st.success(f"✅ Tabela '{nome_tabela}' criada com sucesso!")
            with st.expander(f"👁 Visualizar {nome_tabela}"):
                st.dataframe(df)

        except Exception as e:
            st.error(f"❌ Erro ao processar {uploaded_file.name}: {e}")
