from extract import get_data_municipiosIBGE, get_data_infoDengue
from transform import transform_data_municipios_IBGE, transform_data_infoDengue
from load import create_municipiosIBGE, create_infoDengue, get_municipioId_municipiosIBGE
import logging
import asyncio

logging.basicConfig(level=logging.INFO, filename="logs/pipeline.log", filemode='w', format="%(asctime)s - %(levelname)s - %(message)s", encoding="utf-8")

async def pipeline_municipiosIBGE():
    """
    Executa um pipeline de processamento de dados do IBGE.

    Este pipeline consiste em:
    1. Extrair dados dos municípios brasileiros através da API do IBGE.
    2. Transformar os dados em um DataFrame estruturado para os municípios.
    3. Inserir os dados dos municípios no banco de dados.

    """
    try:
        logging.info('Iniciando pipeline IBGE...')
        data = await get_data_municipiosIBGE()
        if data:
            municipios = await transform_data_municipios_IBGE(data)
            await create_municipiosIBGE(municipios)
            logging.info('Pipeline IBGE executada com sucesso.')
        else:
            logging.error('Nenhum dado foi extraído da API do IBGE.')
    except Exception as e:
        logging.error(f'Erro ao executar pipeline IBGE: {e}')

async def pipeline_infoDengue(ibge_code):
    """
    Executa um pipeline de processamento de dados da Info Dengue para todos os municípios do IBGE.

    Este pipeline consiste em:
    1. Obter todos os municípios cadastrados no banco de dados.
    2. Para cada município, buscar dados de incidência de dengue na API da Info Dengue.
    3. Transformar os dados de dengue em um DataFrame para o município.
    4. Inserir os dados de dengue no banco de dados.

    """
    try:
        data = await get_data_infoDengue(ibge_code)
        if data:
            dengue = await transform_data_infoDengue(data, ibge_code)
            await create_infoDengue(dengue)
            logging.info(f'Pipeline InfoDengue para o município {ibge_code} executada com sucesso.')
        else:
            logging.error(f'Nenhum dado foi extraído da API da Info Dengue para o município {ibge_code}.')
    except Exception as e:
        logging.error(f'Erro ao executar pipeline InfoDengue para o município {ibge_code}: {e}')

async def pipeline():
    await pipeline_municipiosIBGE()

    ibge_codes = get_municipioId_municipiosIBGE()
    tasks = [pipeline_infoDengue(ibge_code) for ibge_code in ibge_codes]

    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(pipeline())