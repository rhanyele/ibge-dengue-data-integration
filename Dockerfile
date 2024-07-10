# Use a imagem base do Python 3.12
FROM python:3.12.2

# Instale o Poetry
RUN pip install poetry

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo pyproject.toml e poetry.lock para o diretório de trabalho
COPY pyproject.toml poetry.lock ./

# Instale as dependências do projeto
RUN poetry install --no-root

# Copie o código fonte para o contêiner
COPY src /app/src

# Crie o diretório de logs
RUN mkdir -p /app/logs

# Exponha a porta 8501 para o Streamlit
EXPOSE 8501

# Comando para iniciar o Streamlit quando o contêiner for iniciado
CMD ["poetry", "run", "streamlit", "run", "--server.port", "8501", "src/app.py"]