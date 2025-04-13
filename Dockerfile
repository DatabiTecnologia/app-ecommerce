# Usa uma imagem base do Python
FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia e instala as dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY app/ ./app/

# Expondo a porta padrão do Streamlit
EXPOSE 8501

# Comando para rodar o Streamlit apontando para o update_data.py
CMD ["streamlit", "run", "app/update_data.py", "--server.port=8501", "--server.address=0.0.0.0"]
