import aiohttp
import logging
from datetime import date

async def extract_api_data(url, params=None):
    """
    Extrai dados de um endpoint de API de forma assíncrona.

    Esta função envia uma requisição GET assíncrona para a URL especificada com os parâmetros fornecidos
    e retorna os dados da resposta em JSON se a requisição for bem-sucedida. Se a requisição
    falhar, ela registra um erro crítico com o código de status.

    Args:
        url (str): A URL do endpoint da API.
        params (dict): Um dicionário de parâmetros a serem enviados com a requisição GET.

    Returns:
        dict or None: Os dados da resposta em JSON se a requisição for bem-sucedida, None se falhar.
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()  # Lança uma exceção para erros HTTP
                logging.info(f"Dados da API {response.url} extraídos com sucesso.")
                return await response.json()
        except aiohttp.ClientResponseError as e:
            logging.critical(f"Erro de resposta ao extrair dados da API {url}: {e}")
        except aiohttp.ClientConnectionError as e:
            logging.critical(f"Erro de conexão ao extrair dados da API {url}: {e}")
        except aiohttp.ClientTimeout as e:
            logging.critical(f"Timeout ao extrair dados da API {url}: {e}")
        except Exception as e:
            if isinstance(e, BaseException):
                logging.critical(f"Erro desconhecido ao extrair dados da API {url}: {e}")
            else:
                logging.critical(f"Erro inesperado ao extrair dados da API {url}: {e}")
        return None

async def get_data_municipiosIBGE():
    """
    Busca dados dos municípios brasileiros a partir da API do IBGE de forma assíncrona.

    Esta função utiliza a função extract_api_data para enviar uma requisição GET para a URL da API do IBGE
    e retorna os dados da resposta em JSON se a requisição for bem-sucedida. Se a requisição falhar,
    um erro será registrado.

    Returns:
        dict or None: Os dados da resposta em JSON se a requisição for bem-sucedida, None se falhar.
    """
    urlIBGE = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
    json_data = await extract_api_data(urlIBGE)
    if json_data:
        logging.info("Dados do IBGE extraídos com sucesso.")
    else:
        logging.error("Falha ao obter dados do IBGE.")
    return json_data

async def get_data_infoDengue(ibge_code, start_year=date.today().year, end_year=date.today().year):
    """
    Busca dados de incidência de dengue de um município brasileiro a partir da API Info Dengue de forma assíncrona.
    Esta função utiliza a função extract_api_data para enviar uma requisição GET para a URL da API Info Dengue
    com os parâmetros específicos de consulta e retorna os dados da resposta em JSON se a requisição for bem-sucedida.
    Se a requisição falhar, um erro será registrado.

    Args:
        ibge_code (str): Código do município do IBGE.
        start_year (int, optional): Ano inicial da consulta (padrão é 2 anos atrás do ano atual).
        end_year (int, optional): Ano final da consulta (padrão é o ano atual).

    Returns:
        dict or None: Os dados da resposta em JSON se a requisição for bem-sucedida, None se falhar.
    """
    params = {
        'geocode': ibge_code,
        'disease': 'dengue',
        'format': 'json',
        'ew_start': '01',
        'ey_start': start_year,
        'ew_end': '53',
        'ey_end': end_year
    }
    urlInfoDengue = "https://info.dengue.mat.br/api/alertcity/"
    json_data = await extract_api_data(urlInfoDengue, params)
    if json_data:
        logging.info(f"Dados de dengue do município: {ibge_code}, período de: {start_year} até {end_year}.")
    else:
        logging.error(f"Falha ao obter dados de dengue do município: {ibge_code}, período de: {start_year} até {end_year}.")
    return json_data