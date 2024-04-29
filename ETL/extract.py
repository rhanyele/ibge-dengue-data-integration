import requests
import logging
from datetime import date

# URL do IBGE
urlIBGE = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
# URL do Info Dengue
urlInfoDengue = "https://info.dengue.mat.br/api/alertcity/"

def extrair_dados_api(url, parametros):
  # Pega a respota da API
  response = requests.get(url, parametros)
  # Valida se o status é 200 = Ok
  if response.status_code == 200: 
    
    # Ler o JSON e extrair os dados
    dadosJson = response.json()
    return(dadosJson)
  
  else:
    logging.critical("Erro ao extrair: ", response.status_code)

def buscar_dados_IBGE():
  # Utiliza a função de busca para trazer os dados do IBGE
  dadosJsonIBGE = extrair_dados_api(urlIBGE, None)
  logging.info("Consegui buscar os dados do IBGE.")
  return(dadosJsonIBGE)

async def buscar_dados_info_dengue(municipio, anoInicial=date.today().year -2, anoFinal=date.today().year):
    # Parâmetros da API
    parametros = {
        'geocode': municipio,   # codigo da cidade do IBGE
        'disease': 'dengue',    # tipo de doença (dengue|chikungunya|zika)
        'format': 'json',       # formato da extração (json|csv)
        'ew_start': '01',       # consulta inicial da semana epidemiológica (1-53)
        'ey_start': anoInicial, # ano da consulta inicial (0-9999)
        'ew_end': '53',         # consulta final da semana epidemiológica (1-53)
        'ey_end': anoFinal      # ano da consulta final (0-9999)
    }
    # Utiliza a função de busca para trazer os dados do Info Dengue passando os parametros
    dadosJsonDengue = extrair_dados_api(urlInfoDengue, parametros)
    logging.info(f"Consegui buscar os dados de dengue do municipio: {municipio}, ano inicial:{anoInicial}, ano final: {anoFinal}.")
    return(dadosJsonDengue)