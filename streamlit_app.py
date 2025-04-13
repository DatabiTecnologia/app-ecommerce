# streamlit_app.py
import os
import sys

# Garante que a pasta 'app/' esteja no caminho
sys.path.insert(0, os.path.abspath("app"))

# Vai chamar a pagina 
from usuario import *
