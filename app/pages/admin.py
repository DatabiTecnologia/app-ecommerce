# app/admin.py

import streamlit as st
import pandas as pd
import psycopg2
from db_utils import conectar_db

st.set_page_config(page_title="Painel do Admin", page_icon="🛠️")

# Funções auxiliares
def excluir_usuario(usuario_id):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
    conn.commit()
    cur.close()
    conn.close()


def cadastrar_usuario(nome, email, senha, tipo):
    conn = conectar_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO usuarios (nome, email, senha, tipo)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (email) DO NOTHING
        """, (nome, email, senha, tipo))
        conn.commit()
        st.success("✅ Usuário cadastrado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao cadastrar: {e}")
    finally:
        cur.close()
        conn.close()

def buscar_usuarios(filtro_email=""):
    conn = conectar_db()
    cur = conn.cursor()
    query = "SELECT id, nome, email, tipo FROM usuarios"
    if filtro_email:
        query += " WHERE email ILIKE %s"
        cur.execute(query, (f"%{filtro_email}%",))
    else:
        cur.execute(query)
    dados = cur.fetchall()
    cur.close()
    conn.close()
    return dados

def inserir_planilha(tabela_nome, arquivo):
    try:
        df = pd.read_excel(arquivo)
        conn = conectar_db()
        cur = conn.cursor()

        # Cria a tabela se não existir (simples - assume todas colunas texto)
        colunas = ", ".join([f"{col} TEXT" for col in df.columns])
        cur.execute(f"CREATE TABLE IF NOT EXISTS {tabela_nome} ({colunas})")

        # Inserção linha por linha
        for _, row in df.iterrows():
            valores = tuple(row.astype(str).values)
            placeholders = ", ".join(["%s"] * len(valores))
            cur.execute(
                f"INSERT INTO {tabela_nome} VALUES ({placeholders})", valores
            )
        conn.commit()
        cur.close()
        conn.close()
        st.success(f"✅ Planilha '{tabela_nome}' inserida no banco com sucesso!")
    except Exception as e:
        st.error(f"Erro ao importar planilha: {e}")

# -------- INTERFACE --------
st.sidebar.title("🛠️ Menu do Administrador")
opcao = st.sidebar.radio("Escolha uma opção:", ["Cadastrar Usuário", "Buscar Usuários", "Subir Planilha"])

if opcao == "Cadastrar Usuário":
    st.title("👤 Cadastro de Novo Usuário")
    nome = st.text_input("Nome")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    tipo = st.selectbox("Tipo de usuário", ["admin", "financeiro", "cliente"])

    if st.button("Cadastrar"):
        cadastrar_usuario(nome, email, senha, tipo)

elif opcao == "Buscar Usuários":
    st.title("🔎 Buscar e Gerenciar Usuários")
    filtro = st.text_input("Buscar por email:")
    usuarios = buscar_usuarios(filtro)

    if usuarios:
        for usuario in usuarios:
            col1, col2, col3, col4, col5 = st.columns([2, 3, 4, 2, 2])
            with col1:
                st.write(usuario[0])  # ID
            with col2:
                st.write(usuario[1])  # Nome
            with col3:
                st.write(usuario[2])  # Email
            with col4:
                st.write(usuario[3])  # Tipo
            with col5:
                if st.button("🗑️ Excluir", key=f"excluir_{usuario[0]}"):
                    if st.confirm(f"Tem certeza que deseja excluir {usuario[2]}?"):
                        excluir_usuario(usuario[0])
                        st.success("Usuário excluído com sucesso!")
                        st.experimental_rerun()
    else:
        st.warning("Nenhum usuário encontrado.")


elif opcao == "Subir Planilha":
    st.title("📤 Subir Planilha para o Banco")
    tabela_nome = st.text_input("Nome da tabela no banco (sem espaços, ex: tb_clientes)")
    arquivo = st.file_uploader("Escolha o arquivo Excel", type=["xlsx"])

    if st.button("Enviar Planilha"):
        if tabela_nome and arquivo:
            inserir_planilha(tabela_nome, arquivo)
        else:
            st.warning("Preencha todos os campos.")
