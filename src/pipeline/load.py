from sqlalchemy import create_engine, Column, Integer, String, Float, BigInteger, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import logging
import os

# Carrega as variáveis de ambiente a partir do arquivo .env
load_dotenv()

# Credenciais do banco de dados
DB_HOST = os.environ['DB_HOST']  # Host onde o banco de dados está rodando
DB_PORT = os.environ['DB_PORT']  # Porta padrão do PostgreSQL
DB_NAME = os.environ['DB_NAME']  # Nome do banco de dados
DB_USER = os.environ['DB_USER']  # Nome do usuário
DB_PASS = os.environ['DB_PASS']  # Senha do usuário

# Configuração do SQLAlchemy
Base = declarative_base()

class MunicipiosIBGE(Base):
    """
    Classe que define o modelo da tabela de municípios.
    """
    __tablename__ = 'municipiosIBGE'

    municipioId = Column(Integer, primary_key=True)
    municipioNome = Column(String)
    estadoNome = Column(String)
    estadoSigla = Column(String)
    regiaoNome = Column(String)
    regiaoSigla = Column(String)

class InfoDengue(Base):
    """
    Classe que define o modelo da tabela de informações de dengue.
    """
    __tablename__ = 'infoDengue'

    infoDengueId = Column(BigInteger, primary_key=True)
    municipioId = Column(Integer, ForeignKey('municipiosIBGE.municipioId'))
    ano = Column(Integer)
    semana = Column(Integer)
    semanaEpidemiologica = Column(String)
    casosEstimados = Column(Float)
    casosEstimadosMin = Column(Float)
    casosEstimadosMax = Column(Float)
    casosNotificados = Column(Float)
    probabilidadeRtMaiorQueUm = Column(Float)
    taxaIncidenciaPor100k = Column(Float)
    nivelAlerta = Column(Float)
    estimativaRt = Column(Float)
    populacaoEstimada = Column(Float)
    temperaturaMinMedia = Column(Float)
    temperaturaMedMedia = Column(Float)
    temperaturaMaxMedia = Column(Float)
    umidadeMinMedia = Column(Float)
    umidadeMedMedia = Column(Float)
    umidadeMaxMedia = Column(Float)
    indicadorReceptividadeClimatica = Column(Float)
    evidenciaTransmissaoSustentada = Column(Float)
    nivelIncidencia = Column(Float)
    casosAcumuladosAno = Column(Float)

def create_db_session():
    """
    Cria uma sessão do SQLAlchemy e conecta ao banco de dados.

    Returns:
        session (Session): Uma sessão do SQLAlchemy.
    """
    try:
        db_url = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        return Session()
    except Exception as e:
        logging.error(f"Erro ao conectar ao banco de dados: {e}")

async def create_municipiosIBGE(df_municipios):
    """
    Insere ou atualiza múltiplos municípios no banco de dados a partir de um DataFrame.

    Args:
        df_municipios (DataFrame): DataFrame contendo os municípios a serem inseridos ou atualizados. 
            Deve conter as colunas:
            - municipioId (int)
            - municipioNome (str)
            - estadoNome (str)
            - estadoSigla (str)
            - regiaoNome (str)
            - regiaoSigla (str)
    """
    session = create_db_session()
    try:
        for index, row in df_municipios.iterrows():
            municipio = session.query(MunicipiosIBGE).filter_by(municipioId=row['municipioId']).first()
            # Se o município existir, atualiza os campos
            if municipio:
                # Atualiza os campos se o município já existir
                municipio.municipioNome = row['municipioNome']
                municipio.estadoNome = row['estadoNome']
                municipio.estadoSigla = row['estadoSigla']
                municipio.regiaoNome = row['regiaoNome']
                municipio.regiaoSigla = row['regiaoSigla']
            else:
                # Insere um novo município se não existir
                municipio = MunicipiosIBGE(
                    municipioId=row['municipioId'],
                    municipioNome=row['municipioNome'],
                    estadoNome=row['estadoNome'],
                    estadoSigla=row['estadoSigla'],
                    regiaoNome=row['regiaoNome'],
                    regiaoSigla=row['regiaoSigla']
                )
                session.add(municipio)
        session.commit()
        logging.info(f"{len(df_municipios)} municípios foram inseridos ou atualizados com sucesso!")
    except Exception as e:
        session.rollback()
        logging.error(f"Erro ao inserir ou atualizar municípios: {e}")
    finally:
        session.close()

async def create_infoDengue(df_infoDengue):
    """
    Insere ou atualiza informações de dengue no banco de dados a partir de um DataFrame.

    Args:
        df_infoDengue (DataFrame): DataFrame contendo os dados de dengue a serem inseridos ou atualizados. 
            Deve conter as colunas:
            - infoDengueId (int)
            - municipioId (int)
            - ano (int)
            - semana (int)
            - semanaEpidemiologica (str)
            - casosEstimados (float)
            - casosEstimadosMin (float)
            - casosEstimadosMax (float)
            - casosNotificados (float)
            - probabilidadeRtMaiorQueUm (float)
            - taxaIncidenciaPor100k (float)
            - nivelAlerta (float)
            - estimativaRt (float)
            - populacaoEstimada (float)
            - temperaturaMinMedia (float)
            - temperaturaMedMedia (float)
            - temperaturaMaxMedia (float)
            - umidadeMinMedia (float)
            - umidadeMedMedia (float)
            - umidadeMaxMedia (float)
            - indicadorReceptividadeClimatica (float)
            - evidenciaTransmissaoSustentada (float)
            - nivelIncidencia (float)
            - casosAcumuladosAno (float)
    """
    session = create_db_session()
    try:
        for index, row in df_infoDengue.iterrows():
            info_dengue = session.query(InfoDengue).filter_by(infoDengueId=row['infoDengueId']).first()
            # Se o registro do info dengue existir, atualiza os campos
            if info_dengue:
                # Atualiza os campos se o registro de dengue já existir
                info_dengue.municipioId = row['municipioId']
                info_dengue.ano = row['ano']
                info_dengue.semana = row['semana']
                info_dengue.semanaEpidemiologica = row['semanaEpidemiologica']
                info_dengue.casosEstimados = row['casosEstimados']
                info_dengue.casosEstimadosMin = row['casosEstimadosMin']
                info_dengue.casosEstimadosMax = row['casosEstimadosMax']
                info_dengue.casosNotificados = row['casosNotificados']
                info_dengue.probabilidadeRtMaiorQueUm = row['probabilidadeRtMaiorQueUm']
                info_dengue.taxaIncidenciaPor100k = row['taxaIncidenciaPor100k']
                info_dengue.nivelAlerta = row['nivelAlerta']
                info_dengue.estimativaRt = row['estimativaRt']
                info_dengue.populacaoEstimada = row['populacaoEstimada']
                info_dengue.temperaturaMinMedia = row['temperaturaMinMedia']
                info_dengue.temperaturaMedMedia = row['temperaturaMedMedia']
                info_dengue.temperaturaMaxMedia = row['temperaturaMaxMedia']
                info_dengue.umidadeMinMedia = row['umidadeMinMedia']
                info_dengue.umidadeMedMedia = row['umidadeMedMedia']
                info_dengue.umidadeMaxMedia = row['umidadeMaxMedia']
                info_dengue.indicadorReceptividadeClimatica = row['indicadorReceptividadeClimatica']
                info_dengue.evidenciaTransmissaoSustentada = row['evidenciaTransmissaoSustentada']
                info_dengue.nivelIncidencia = row['nivelIncidencia']
                info_dengue.casosAcumuladosAno = row['casosAcumuladosAno']
            else:
                # Insere um novo registro se não existir
                info_dengue = InfoDengue(
                    infoDengueId=row['infoDengueId'],
                    municipioId=row['municipioId'],
                    ano=row['ano'],
                    semana=row['semana'],
                    semanaEpidemiologica=row['semanaEpidemiologica'],
                    casosEstimados=row['casosEstimados'],
                    casosEstimadosMin=row['casosEstimadosMin'],
                    casosEstimadosMax=row['casosEstimadosMax'],
                    casosNotificados=row['casosNotificados'],
                    probabilidadeRtMaiorQueUm=row['probabilidadeRtMaiorQueUm'],
                    taxaIncidenciaPor100k=row['taxaIncidenciaPor100k'],
                    nivelAlerta=row['nivelAlerta'],
                    estimativaRt=row['estimativaRt'],
                    populacaoEstimada=row['populacaoEstimada'],
                    temperaturaMinMedia=row['temperaturaMinMedia'],
                    temperaturaMedMedia=row['temperaturaMedMedia'],
                    temperaturaMaxMedia=row['temperaturaMaxMedia'],
                    umidadeMinMedia=row['umidadeMinMedia'],
                    umidadeMedMedia=row['umidadeMedMedia'],
                    umidadeMaxMedia=row['umidadeMaxMedia'],
                    indicadorReceptividadeClimatica=row['indicadorReceptividadeClimatica'],
                    evidenciaTransmissaoSustentada=row['evidenciaTransmissaoSustentada'],
                    nivelIncidencia=row['nivelIncidencia'],
                    casosAcumuladosAno=row['casosAcumuladosAno']
                )
                session.add(info_dengue)
        session.commit()
        logging.info(f"{len(df_infoDengue['municipioId'])} dados de dengue foram inseridos ou atualizados com sucesso!")
    except Exception as e:
        session.rollback()
        logging.error(f"Erro ao inserir ou atualizar dados de dengue: {e}")
    finally:
        session.close()


def get_all_infoDengue():
    """
    Obtem todos os dados de dengue do banco de dados.

    Args:
        session (Session): Sessão do SQLAlchemy.

    Returns:
        infoDengue (list): Uma lista de todos os dados de dengue.
    """
    session = create_db_session()
    try:
        infoDengue = session.query(InfoDengue).all()
        return infoDengue
    except Exception as e:
        logging.error(f"Erro ao obter dados de dengue: {e}")

def get_all_municipiosIBGE():
    """
    Obtem todos os municípios do banco de dados.

    Args:
        session (Session): Sessão do SQLAlchemy.

    Returns:
        municipios (list): Uma lista de todos os municípios.
    """
    session = create_db_session()
    try:
        municipios = session.query(MunicipiosIBGE).all()
        return municipios
    except Exception as e:
        logging.error(f"Erro ao obter municípios: {e}")

def get_municipioId_municipiosIBGE():
    """
    Obtem todos os IDs dos municípios do banco de dados.

    Returns:
        municipioIds (list): Uma lista de todos os IDs dos municípios.
    """
    session = create_db_session()
    try:
        municipioIds = session.query(MunicipiosIBGE.municipioId).distinct().all()
        return [m[0] for m in municipioIds]
    except Exception as e:
        logging.error(f"Erro ao obter IDs dos municípios: {e}")
    finally:
        session.close()