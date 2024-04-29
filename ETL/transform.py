import pandas as pd
import logging

def transformar_dados_IBGE(dadosJSON):
  # Transforma o Json em DataFrame
  dadosJSON = pd.DataFrame(dadosJSON)
  try:
    # Criar um DataFrame de Municipios
    municipios_df = pd.DataFrame({
      'municipioId': dadosJSON.apply(lambda x: x['id'], axis=1),
      'municipioNome': dadosJSON.apply(lambda x: x['nome'], axis=1),
      'estadoNome': dadosJSON['microrregiao'].apply(lambda x: x['mesorregiao']['UF']['nome']),
      'estadoSigla': dadosJSON['microrregiao'].apply(lambda x: x['mesorregiao']['UF']['sigla']),
      'regiaoNome': dadosJSON['microrregiao'].apply(lambda x: x['mesorregiao']['UF']['regiao']['nome']),
      'regiaoSigla': dadosJSON['microrregiao'].apply(lambda x: x['mesorregiao']['UF']['regiao']['sigla'])
    })
    logging.info('Dados tratados e DataFrame de municipios criado.')
    return(municipios_df)
  except Exception as erro:
    logging.critical(f"Erro ao transformar municipios:: {erro}")
    

async def transformar_dados_dengue(dadosJSON, municipio):
  # Transforma o Json em DataFrame
  dadosJSON = pd.DataFrame(dadosJSON)
  try:
    # Cria um DataFrame para os casos de dengue
    dengue_df = pd.DataFrame({
      
      'municipioId': municipio, # Código do IBGE
      'dataInicialSemanaEpidemiologica': dadosJSON['data_iniSE'], # Primeiro dia da semana epidemiológica (Domingo)
      'semanaEpidemiologica': dadosJSON['SE'], # Semana epidemiológica
      'casosEstimados': dadosJSON['casos_est'], # Número estimado de casos por semana usando o modelo de nowcasting (nota: Os valores são atualizados retrospectivamente a cada semana)
      'casosEstimadosMin': dadosJSON['casos_est_min'], # Intervalo minimo de credibilidade de 95% do número estimado de casos
      'casosEstimadosMax': dadosJSON['casos_est_max'], # Intervalo maximo de credibilidade de 95% do número estimado de casos
      'casosNotificados': dadosJSON['casos'], # Número de casos notificados por semana (Os valores são atualizados retrospectivamente todas as semanas)
      'probabilidadeRtMaiorQueUm': dadosJSON['p_rt1'], # Probabilidade de (Rt> 1). Para emitir o alerta laranja, usamos o critério p_rt1> 0,95 por 3 semanas ou mais
      'taxaIncidenciaPor100k': dadosJSON['p_inc100k'], # Taxa de incidência estimada por 100.000
      # 'localidadeID': dadosJSON['Localidade_id'], # Divisão submunicipal (atualmente implementada apenas no Rio de Janeiro)
      'nivelAlerta': dadosJSON['nivel'], # Nível de alerta (1 = verde, 2 = amarelo, 3 = laranja, 4 = vermelho)
      # 'ID': dadosJSON['id'], # Índice numérico
      # 'versaoModelo': dadosJSON['versao_modelo'], # Versão do modelo (uso interno da API)
      'estimativaRt': dadosJSON['Rt'], # Estimativa pontual do número reprodutivo de casos
      'populacaoEstimada': dadosJSON['pop'], # População estimada (IBGE)
      'temperaturaMinMedia': dadosJSON['tempmin'], # Média das temperaturas mínimas diárias ao longo da semana
      'temperaturaMedMedia': dadosJSON['tempmed'], # Média das temperaturas diárias ao longo da semana
      'temperaturaMaxMedia': dadosJSON['tempmax'], # Média das temperaturas máximas diárias ao longo da semana
      'umidadeMinMedia': dadosJSON['umidmin'], # Média da umidade relativa mínima diária do ar ao longo da semana
      'umidadeMedMedia': dadosJSON['umidmed'], # Média da umidade relativa diária do ar ao longo da semana
      'umidadeMaxMedia': dadosJSON['umidmax'], # Média da umidade relativa máxima diária do ar ao longo da semana
      'indicadorReceptividadeClimatica': dadosJSON['receptivo'], # Indica receptividade climática, ou seja, condições para alta capacidade vetorial. 0 = desfavorável, 1 = favorável, 2 = favorável nesta semana e na semana passada, 3 = favorável por pelo menos três semanas (suficiente para completar um ciclo de transmissão)
      'evidenciaTransmissaoSustentada': dadosJSON['transmissao'], # Evidência de transmissão sustentada: 0 = nenhuma evidência, 1 = possível, 2 = provável, 3 = altamente provável
      'nivelIncidencia': dadosJSON['nivel_inc'], # Incidência estimada abaixo do limiar pré-epidemia, 1 = acima do limiar pré-epidemia, mas abaixo do limiar epidêmico, 2 = acima do limiar epidêmico
      'casosAcumuladosAno': dadosJSON['notif_accum_year'] # Número acumulado de casos no ano
      })
    
    # Extrair o ano e a semana
    dengue_df['ano'] = dengue_df['semanaEpidemiologica'] // 100
    dengue_df['semana'] = dengue_df['semanaEpidemiologica'] % 100
    # Trata a semana epdemiologgica para o formato semana/ano 
    dengue_df['semanaEpidemiologica'] = dengue_df['semanaEpidemiologica'].apply(lambda x: f"{(x % 100):02d}/{x // 100}")
    # Arredonda os dados para 2 casas decimais
    dengue_df['probabilidadeRtMaiorQueUm'] = round(dengue_df['probabilidadeRtMaiorQueUm'], 2)
    dengue_df['taxaIncidenciaPor100k'] = round(dengue_df['taxaIncidenciaPor100k'], 2)
    dengue_df['estimativaRt'] = round(dengue_df['estimativaRt'], 2)
    dengue_df['temperaturaMinMedia'] = round(dengue_df['temperaturaMinMedia'], 2)
    dengue_df['temperaturaMedMedia'] = round(dengue_df['temperaturaMedMedia'], 2)
    dengue_df['temperaturaMaxMedia'] = round(dengue_df['temperaturaMaxMedia'], 2)
    dengue_df['umidadeMinMedia'] = round(dengue_df['umidadeMinMedia'], 2)
    dengue_df['umidadeMedMedia'] = round(dengue_df['umidadeMedMedia'], 2)
    dengue_df['umidadeMaxMedia'] = round(dengue_df['umidadeMaxMedia'], 2)

    logging.info(f'Dados tratados e DataFrame de dengue criado para o municipio: {municipio}.')
    return(dengue_df) 
  except Exception as erro:
    logging.critical(f"Erro ao transformar dengue: {erro}")