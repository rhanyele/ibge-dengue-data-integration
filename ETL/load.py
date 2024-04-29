from sqlalchemy import create_engine
from pandas import read_sql_table
from dotenv import load_dotenv
import logging
import os

load_dotenv()

DB_HOST = os.environ['DB_HOST'] # Host onde o banco de dados está rodando
DB_PORT = os.environ['DB_PORT'] # Porta padrão do PostgreSQL
DB_NAME = os.environ['DB_NAME'] # Nome do banco de dados
DB_USER = os.environ['DB_USER'] # Nome do usuário
DB_PASS = os.environ['DB_PASS'] # Senha do usuário

# Cria uma engine para o metodo to_sql do pandas conseguir persistir no banco de dados postgres
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

async def salvar_dados(dados, tabela):
    try:
        # Salva o DataFrame na tabela do banco de dados usando o método 'multi' para upsert
        # Configura 'index' como False para evitar adicionar índices duplicados
        # if_exists: como 'replace' para adicionar ou atualizar novos registros, 'append' adiciona os novos registro na tabela
        # index: cria uma coluna de indice
        # method: passa vários valores em uma única cláusula INSERT
        # chunksize: especifica o número de linhas em cada lote a serem inseridas
        dados.to_sql(tabela, engine, if_exists='append', index=False, chunksize=500, method='multi')
        logging.info(f"Dados inseridos ou atualizados na tabela {tabela} com sucesso!")
    except Exception as erro:
        logging.critical(f"Erro ao inserir os dados na tabela {tabela}: {erro}")

def listar_tabela(tabela):
    try:
        dados = read_sql_table(tabela, engine)
        logging.info(f'Dados carregados da tabela {tabela}.')
        return(dados)
    except Exception as erro:
        logging.critical(f"Erro ao ler os dados da tabela {tabela}: {erro}")   