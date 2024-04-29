from ETL.extract import buscar_dados_IBGE, buscar_dados_info_dengue
from ETL.transform import transformar_dados_IBGE, transformar_dados_dengue
from ETL.load import salvar_dados, listar_tabela
import logging

logging.basicConfig(level=logging.INFO, filename=".log", filemode='w', format="%(asctime)s - %(levelname)s - %(message)s")

def pipeline_IBGE():
    # Busca os dados na API do IBGE
    dados = buscar_dados_IBGE()

    municipios = transformar_dados_IBGE(dados)

    tabela = 'municipiosIBGE'
    salvar_dados(municipios, tabela)

    logging.info('Pipeline IBGGE executada com sucesso.')

def pipeline_info_dengue():
    # Listar dos os municipios do IBGE
    tabelaMunicipio = 'municipiosIBGE'
    municipios = listar_tabela(tabelaMunicipio)

    # Busca os dados na API do Info Dengue
    for municipio in municipios['municipioId']:
        dados = buscar_dados_info_dengue(municipio)
        tabelaInfoDengue = 'InfoDengue'
        dengue = transformar_dados_dengue(dados, municipio)
        salvar_dados(dengue, tabelaInfoDengue)

    logging.info('Pipeline InfoDengue executada com sucesso.')

if __name__ == '__main__':
    logging.info('########## INICIO DA EXECUCAO ##########')
    pipeline_IBGE()
    pipeline_info_dengue()
    logging.info('########## FIM DA EXECUCAO ##########')
