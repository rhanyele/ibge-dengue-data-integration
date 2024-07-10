import pandas as pd
import logging

async def transform_data_municipios_IBGE(json):
    """
    Transforma dados do IBGE em um DataFrame.

    Args:
        json (list): Lista de dicionários contendo dados do IBGE.

    Returns:
        pd.DataFrame or None: DataFrame dos municípios se a transformação for bem-sucedida, None se ocorrer um erro.
    """
    try:
        data = pd.DataFrame(json)
        municipios_df = pd.DataFrame({
            'municipioId': data.apply(lambda x: x['id'], axis=1),
            'municipioNome': data.apply(lambda x: x['nome'], axis=1),
            'municipioNomeEstadoSigla': data.apply(lambda x: x['nome'], axis=1) + ' - ' + data['microrregiao'].apply(lambda x: x['mesorregiao']['UF']['sigla']),
            'estadoNome': data['microrregiao'].apply(lambda x: x['mesorregiao']['UF']['nome']),
            'estadoSigla': data['microrregiao'].apply(lambda x: x['mesorregiao']['UF']['sigla']),
            'regiaoNome': data['microrregiao'].apply(lambda x: x['mesorregiao']['UF']['regiao']['nome']),
            'regiaoSigla': data['microrregiao'].apply(lambda x: x['mesorregiao']['UF']['regiao']['sigla'])
        })
        logging.info('Dados tratados e DataFrame de municípios criado.')
        return municipios_df
    except Exception as erro:
        logging.critical(f"Erro ao transformar dados do IBGE: {erro}")
        return None

async def transform_data_infoDengue(json, ibge_code):
    """
    Transforma dados de incidência de dengue em um DataFrame.

    Args:
        json (list): Lista de dicionários contendo dados de incidência de dengue.
        ibge_code (str): Código do município do IBGE.

    Returns:
        pd.DataFrame or None: DataFrame dos casos de dengue se a transformação for bem-sucedida, None se ocorrer um erro.
    """
    try:
        data = pd.DataFrame(json)
        dengue_df = pd.DataFrame({
            'municipioId': ibge_code, # Código do IBGE
            'casosEstimados': data['casos_est'], # Número estimado de casos por semana usando o modelo de nowcasting (nota: Os valores são atualizados retrospectivamente a cada semana)
            'casosEstimadosMin': data['casos_est_min'], # Intervalo minimo de credibilidade de 95% do número estimado de casos
            'casosEstimadosMax': data['casos_est_max'], # Intervalo maximo de credibilidade de 95% do número estimado de casos
            'casosNotificados': data['casos'], # Número de casos notificados por semana (Os valores são atualizados retrospectivamente todas as semanas)
            'probabilidadeRtMaiorQueUm': round(data['p_rt1'], 2), # Probabilidade de (Rt> 1). Para emitir o alerta laranja, usamos o critério p_rt1> 0,95 por 3 semanas ou mais
            'taxaIncidenciaPor100k': round(data['p_inc100k'], 2), # Taxa de incidência estimada por 100.000
            'nivelAlerta': data['nivel'], # Nível de alerta (1 = verde, 2 = amarelo, 3 = laranja, 4 = vermelho)
            'infoDengueId': data['id'], # Índice numérico
            'estimativaRt': round(data['Rt'], 2), # Estimativa pontual do número reprodutivo de casos
            'populacaoEstimada': data['pop'], # População estimada (IBGE)
            'temperaturaMinMedia': round(data['tempmin'], 2), # Média das temperaturas mínimas diárias ao longo da semana
            'temperaturaMedMedia': round(data['tempmed'], 2), # Média das temperaturas diárias ao longo da semana
            'temperaturaMaxMedia': round(data['tempmax'], 2), # Média das temperaturas máximas diárias ao longo da semana
            'umidadeMinMedia': round(data['umidmin'], 2), # Média da umidade relativa mínima diária do ar ao longo da semana
            'umidadeMedMedia': round(data['umidmed'], 2), # Média da umidade relativa diária do ar ao longo da semana
            'umidadeMaxMedia': round(data['umidmax'], 2), # Média da umidade relativa máxima diária do ar ao longo da semana
            'indicadorReceptividadeClimatica': data['receptivo'], # Indica receptividade climática, ou seja, condições para alta capacidade vetorial. 0 = desfavorável, 1 = favorável, 2 = favorável nesta semana e na semana passada, 3 = favorável por pelo menos três semanas (suficiente para completar um ciclo de transmissão)
            'evidenciaTransmissaoSustentada': data['transmissao'], # Evidência de transmissão sustentada: 0 = nenhuma evidência, 1 = possível, 2 = provável, 3 = altamente provável
            'nivelIncidencia': data['nivel_inc'], # Incidência estimada abaixo do limiar pré-epidemia, 1 = acima do limiar pré-epidemia, mas abaixo do limiar epidêmico, 2 = acima do limiar epidêmico
            'casosAcumuladosAno': data['notif_accum_year'], # Número acumulado de casos no ano
            'ano': data['SE'] // 100, # Extraindo o ano da semana epidemiológica
            'semana': data['SE'] % 100, # Extraindo a semana da semana epidemiológica
            'semanaEpidemiologica': data['SE'].apply(lambda x: f"{(x % 100):02d}/{x // 100}") # Formatando a semana epidemiológica para o formato semana/ano
        })
        logging.info(f'Dados tratados e DataFrame de dengue criado para o município: {ibge_code}.')
        return dengue_df
    except Exception as erro:
        logging.critical(f"Erro ao transformar dados de dengue para o município {ibge_code}: {erro}")
        return None