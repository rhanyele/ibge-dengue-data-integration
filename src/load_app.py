import streamlit as st
import pandas as pd
from pipeline.load import get_all_municipiosIBGE, get_all_infoDengue

# Converter colunas numéricas para tipos adequados
numeric_columns = [
    "casosEstimados", "casosEstimadosMin", "casosEstimadosMax", "casosNotificados",
    "probabilidadeRtMaiorQueUm", "taxaIncidenciaPor100k", "estimativaRt", "populacaoEstimada",
    "temperaturaMinMedia", "temperaturaMedMedia", "temperaturaMaxMedia",
    "umidadeMinMedia", "umidadeMedMedia", "umidadeMaxMedia",
    "indicadorReceptividadeClimatica", "evidenciaTransmissaoSustentada", "casosAcumuladosAno"
]

# Rótulos para as colunas
labels_columns = {
    "ano": "Ano",
    "semanaEpidemiologica": "Semana Epidemiológica",
    "regiaoNome": "Região",
    "estadoNome": "Estado",
    "municipioNome": "Município",
    "casosEstimados": "Casos Estimados",
    "casosEstimadosMin": "Casos Estimados (Mín)",
    "casosEstimadosMax": "Casos Estimados (Máx)",
    "casosNotificados": "Casos Notificados",
    "probabilidadeRtMaiorQueUm": "Probabilidade de Rt > 1",
    "taxaIncidenciaPor100k": "Taxa de Incidência por 100k Habitantes",
    "estimativaRt": "Estimativa de Rt",
    "populacaoEstimada": "População Estimada",
    "temperaturaMinMedia": "Temperatura Mínima Média",
    "temperaturaMedMedia": "Temperatura Média Média",
    "temperaturaMaxMedia": "Temperatura Máxima Média",
    "umidadeMinMedia": "Umidade Mínima Média",
    "umidadeMedMedia": "Umidade Média Média",
    "umidadeMaxMedia": "Umidade Máxima Média",
    "indicadorReceptividadeClimatica": "Indicador de Receptividade Climática",
    "evidenciaTransmissaoSustentada": "Evidência de Transmissão Sustentada",
    "casosAcumuladosAno": "Casos Acumulados por Ano"
}


def municipios_dataframe():
    """
    Obtém todos os municípios do banco de dados e os coloca em um DataFrame do Pandas.

    Returns:
        df_municipios (DataFrame): DataFrame contendo todos os municípios.
    """
    municipios = get_all_municipiosIBGE()
    # Extrair os dados para um DataFrame
    data = [
        {
            'municipioId': municipio.municipioId,
            'municipioNome': municipio.municipioNome,
            'estadoNome': municipio.estadoNome,
            'estadoSigla': municipio.estadoSigla,
            'regiaoNome': municipio.regiaoNome,
            'regiaoSigla': municipio.regiaoSigla
        }
        for municipio in municipios
    ]
    df_municipios = pd.DataFrame(data)
    return df_municipios

def infodengue_dataframe():
    """
    Obtém todos os dados de dengue do banco de dados e os coloca em um DataFrame do Pandas.

    Returns:
        df_infoDengue (DataFrame): DataFrame contendo todos os dados de dengue.
    """
    infoDengue = get_all_infoDengue()
    # Extrair os dados para um DataFrame
    data = [
        {
            'infoDengueId': info.infoDengueId,
            'municipioId': info.municipioId,
            'ano': info.ano,
            'semana': info.semana,
            'semanaEpidemiologica': info.semanaEpidemiologica,
            'casosEstimados': info.casosEstimados,
            'casosEstimadosMin': info.casosEstimadosMin,
            'casosEstimadosMax': info.casosEstimadosMax,
            'casosNotificados': info.casosNotificados,
            'probabilidadeRtMaiorQueUm': info.probabilidadeRtMaiorQueUm,
            'taxaIncidenciaPor100k': info.taxaIncidenciaPor100k,
            'nivelAlerta': info.nivelAlerta,
            'estimativaRt': info.estimativaRt,
            'populacaoEstimada': info.populacaoEstimada,
            'temperaturaMinMedia': info.temperaturaMinMedia,
            'temperaturaMedMedia': info.temperaturaMedMedia,
            'temperaturaMaxMedia': info.temperaturaMaxMedia,
            'umidadeMinMedia': info.umidadeMinMedia,
            'umidadeMedMedia': info.umidadeMedMedia,
            'umidadeMaxMedia': info.umidadeMaxMedia,
            'indicadorReceptividadeClimatica': info.indicadorReceptividadeClimatica,
            'evidenciaTransmissaoSustentada': info.evidenciaTransmissaoSustentada,
            'nivelIncidencia': info.nivelIncidencia,
            'casosAcumuladosAno': info.casosAcumuladosAno
        }
        for info in infoDengue
    ]
    df_infoDengue = pd.DataFrame(data)
    return df_infoDengue

# Carregar os dados em cache
@st.cache_data()
def load_data_municipios():
    infodengue = infodengue_dataframe()
    municipios = municipios_dataframe()
    if infodengue.empty or municipios.empty:
        return []  
    else:
        data = pd.merge(municipios, infodengue, on='municipioId', how='inner')
        # Converter colunas numéricas para tipos adequados
        for col in numeric_columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
        return data