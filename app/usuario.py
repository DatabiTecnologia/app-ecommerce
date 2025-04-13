# app/usuario.py

import streamlit as st
import psycopg2
from db_utils import conectar_db
from PIL import Image

st.set_page_config(page_title="Login", page_icon="🛍️", layout="centered")

def validar_login(email, senha):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, nome, tipo FROM usuarios 
        WHERE email = %s AND senha = %s
    """, (email, senha))
    usuario = cur.fetchone()
    cur.close()
    conn.close()
    return usuario

# 🎨 Estilo personalizado
st.markdown("""
    <style>
        .main {
            background-color: #000000;
            color: white;
        }
        .stApp {
            background-color: #000000;
            color: white;
        }
        h2.title {
            animation: pulse 2s infinite;
            color: #FFD700;
            text-align: center;
            font-family: 'Arial', sans-serif;
            font-size: 28px;
            margin-top: 20px;
        }
        @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.05); opacity: 0.8; }
            100% { transform: scale(1); opacity: 1; }
        }
        .stTextInput > div > div > input {
            background-color: #1a1a1a;
            color: white;
        }
        .stTextInput label {
            color: white;
        }
        .stButton button {
            background-color: #FFD700;
            color: black;
            font-weight: bold;
            border-radius: 8px;
        }
        .stButton button:hover {
            background-color: #FFC300;
            transform: scale(1.02);
        }
    </style>
""", unsafe_allow_html=True)

# 🖼️ Logo
logo = Image.open("app/logo.png")
st.image(logo, width=150)

# ✨ Título animado
st.markdown("<h2 class='title'>Bem-vindo à Nossa Empresa de E-commerce</h2>", unsafe_allow_html=True)

# 🔐 Formulário de login
if "usuario_logado" not in st.session_state:
    st.subheader("Acesso ao Sistema")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        usuario = validar_login(email, senha)
        if usuario:
            st.session_state["usuario_logado"] = {
                "id": usuario[0],
                "nome": usuario[1],
                "tipo": usuario[2]
            }
            st.success(f"Bem-vindo, {usuario[1]} ({usuario[2]})!")
            st.experimental_rerun()
        else:
            st.error("Email ou senha inválidos.")

# ✅ Se já estiver logado
else:
    user = st.session_state["usuario_logado"]
    st.success(f"Você está logado como {user['nome']} ({user['tipo']})")

    if st.button("Ir para o painel"):
        if user["tipo"] == "admin":
            st.switch_page("pages/admin.py")
        elif user["tipo"] == "financeiro":
            st.switch_page("pages/financeiro.py")
        elif user["tipo"] == "cliente":
            st.switch_page("app/cliente.py")
        else:
            st.warning("Tipo de usuário não reconhecido.")

    if st.button("Logout"):
        del st.session_state["usuario_logado"]
        st.experimental_rerun()
