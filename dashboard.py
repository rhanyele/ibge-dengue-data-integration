import pandas as pd
import plotly.express as px
import streamlit as st
from ETL.load import listar_tabela

# Título da página e o layout como wide
st.set_page_config(page_title="Meu Dashboard",layout="wide")

# Carregar os dados
info_dengue = listar_tabela('InfoDengue')
municipios_ibge = listar_tabela('municipiosIBGE')

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

# Combinar os DataFrames
df = pd.merge(municipios_ibge, info_dengue, on='municipioId', how='inner')

# Converter colunas numéricas para tipos adequados
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Função para aplicar filtros
def aplicar_filtros(df, ano_filtrado, regiao_filtrada, estado_filtrado, municipio_filtrado):
    df_filtrado = df[
        (df['ano'] == ano_filtrado) &
        (df['regiaoNome'] == regiao_filtrada) &
        (df['estadoNome'] == estado_filtrado) &
        (df['municipioNome'] == municipio_filtrado)
    ].reset_index(drop=True)
    return df_filtrado

# Filtro por ano
ano_filtrado = st.sidebar.selectbox('Selecione o Ano', df['ano'].unique())

# Filtrar dados para o ano selecionado
df_ano_filtrado = df[df['ano'] == ano_filtrado]

# Filtro por região
regiao_filtrada = st.sidebar.selectbox('Selecione a Região', df_ano_filtrado['regiaoNome'].unique())

# Filtrar estados com base na região selecionada
estados_regiao = df_ano_filtrado[df_ano_filtrado['regiaoNome'] == regiao_filtrada]['estadoNome'].unique()
estado_filtrado = st.sidebar.selectbox('Selecione o Estado', estados_regiao)

# Filtrar municípios com base no estado selecionado
municipios_estado = df_ano_filtrado[df_ano_filtrado['estadoNome'] == estado_filtrado]['municipioNome'].unique()
municipio_filtrado = st.sidebar.selectbox('Selecione o Município', municipios_estado)

# Aplicar filtros
df_filtrado = aplicar_filtros(df_ano_filtrado, ano_filtrado, regiao_filtrada, estado_filtrado, municipio_filtrado)

# Ordenar o DataFrame pela coluna 'semanaEpidemiologica'
df_filtrado = df_filtrado.sort_values(by='semanaEpidemiologica').reset_index(drop=True)



# Título do dashboard
st.title('Monitoramento Epidemiológico:')
st.subheader(f'Análise do município de {municipio_filtrado}, estado de {estado_filtrado}, ano de {ano_filtrado}.')
st.caption('Dados extraídos do [InfoDengue](https://info.dengue.mat.br/) e [IBGE](https://www.ibge.gov.br/).')

st.divider()

# Restante do código para plotar os gráficos

# Gráfico 1: Comparação entre Casos Estimados e Casos Notificados por Semana
st.subheader('Comparação entre Casos Estimados e Casos Notificados por Semana')
st.caption('Número de casos notificados, número de casos estimados usando o modelo de nowcasting e intervalo de credibilidade de 95% do número de casos estimados.')
fig1 = px.line(df_filtrado, x='semanaEpidemiologica', y=['casosEstimados', 'casosNotificados'], labels=labels_columns)
fig1.add_scatter(x=df_filtrado['semanaEpidemiologica'], y=df_filtrado['casosEstimadosMin'], 
                 mode='lines', line=dict(dash='dash'), name='casosEstimadosMin')
fig1.add_scatter(x=df_filtrado['semanaEpidemiologica'], y=df_filtrado['casosEstimadosMax'], 
                 mode='lines', line=dict(dash='dash'), name='casosEstimadosMax')
st.plotly_chart(fig1)

# Gráfico 2: Probabilidade de Rt > 1 por Semana
st.subheader('Probabilidade de Rt > 1 por Semana')
st.caption('Probabilidade de (Rt > 1). Para emitir o alerta laranja, usamos o critério p_rt1 > 0,95 por 3 semanas ou mais.')
fig2 = px.line(df_filtrado, x='semanaEpidemiologica', y='probabilidadeRtMaiorQueUm', text='probabilidadeRtMaiorQueUm', labels=labels_columns)
fig2.update_traces(fill='tozeroy', textposition='top right')
fig2.add_shape(
    type='line',
    x0=df_filtrado['semanaEpidemiologica'].min(),
    y0=0.95,
    x1=df_filtrado['semanaEpidemiologica'].max(),
    y1=0.95,
    line=dict(color='red', dash='dash')
)
# Configurações de layout
fig2.update_layout(yaxis_tickvals=[])
st.plotly_chart(fig2)

# Gráfico 3: Taxa de Incidência por 100.000 Habitantes por Semana
st.subheader('Taxa de Incidência por 100.000 Habitantes por Semana')
st.caption('Taxa de incidência estimada por 100.000 habitantes')
fig3 = px.line(df_filtrado, x='semanaEpidemiologica', y='taxaIncidenciaPor100k', text='taxaIncidenciaPor100k', labels=labels_columns)
# Adicionar rótulos de valores aos pontos de dados
fig3.update_traces(textposition='top right')
fig2.update_traces(marker=dict(color='orange'), selector=dict(type='scatter', mode='markers', y='probabilidadeRtMaiorQueUm', y0=0.95))
# Configurações de layout
fig3.update_layout(yaxis_tickvals=[])
st.plotly_chart(fig3)

# Gráfico 4: Evidência de Transmissão Sustentada
st.subheader('Evidência de Transmissão Sustentada por Semana')
# Definindo a regra de cores e a legenda
legenda_evidencia = {
    0: '0 - Nenhuma evidência',
    1: '1 - Possível',
    2: '2 - Provável',
    3: '3 - Altamente provável'
}
# Criar DataFrame apenas com as colunas necessárias
df_tabela = df_filtrado[['semanaEpidemiologica', 'evidenciaTransmissaoSustentada']]
# Mapear os valores numéricos para suas respectivas legendas
df_tabela['Evidência de Transmissão Sustentada'] = df_tabela['evidenciaTransmissaoSustentada'].map(legenda_evidencia)
# Remover a coluna de valores numéricos
df_tabela.drop(columns=['evidenciaTransmissaoSustentada'], inplace=True)
# Renomear as colunas
df_tabela.columns = ['Semana Epidemiológica', 'Evidência de Transmissão Sustentada']
# Exibir a tabela
st.write(df_tabela)

# Gráfico 5: Mapa de Calor: Indicador Receptividade Climática dos municípios do estado
st.subheader('Indicador Receptividade Climática')
st.caption('Legenda:\n0 = desfavorável,\n1 = favorável,\n2 = favorável nesta semana e na semana passada,\n3 = favorável por pelo menos três semanas (suficiente para completar um ciclo de transmissão).')
df_filtrado_estado = df_ano_filtrado[df_ano_filtrado['estadoNome'] == estado_filtrado]
fig5 = px.imshow(df_filtrado_estado[['semanaEpidemiologica', 'municipioNome', 'indicadorReceptividadeClimatica']].pivot_table(index='municipioNome', columns='semanaEpidemiologica', values='indicadorReceptividadeClimatica'), 
                        labels=labels_columns, color_continuous_scale=['#01DB3B', '#DB0006'])
# Ajustando as dimensões do layout do gráfico
fig5.update_layout(height=1000, coloraxis=dict(
                              cmin=0, # Define o limite mínimo da escala de cores  
                              cmax=3  # Define o limite máximo da escala de cores
                              ))
# Exibindo o gráfico centralizado
st.plotly_chart(fig5, use_container_width=True, align='center')

# Gráfico 6: Casos Acumulados por Ano (considerando o filtro de município)
st.subheader('Casos Acumulados por Ano no Município')
st.caption('Número acumulado de casos notificados no ano.')
# Pega o DataFrame principal e filtra o município
df_filtrado_municipio = df[(df['municipioNome'] == municipio_filtrado)]
# Soma todos os casos notificados do ano 
df_casos_acumulados_por_ano = df_filtrado_municipio.groupby('ano')['casosNotificados'].sum().reset_index()
# Montando o gráfico de barras
fig6 = px.bar(df_casos_acumulados_por_ano, x='ano', y='casosNotificados', text='casosNotificados', labels=labels_columns)
fig6.update_xaxes(tickformat="d")  # Definir a escala do eixo x como inteiros
fig6.update_layout(yaxis_tickvals=[])
st.plotly_chart(fig6)

# Título da tabela de resumo
st.subheader('Tabela de Resumo dos Dados')
# Lista de colunas utilizadas em todos os gráficos
colunas_utilizadas = [
    "semanaEpidemiologica", "regiaoNome", "estadoNome", "municipioNome",
    "casosEstimados", "casosEstimadosMin", "casosEstimadosMax", "casosNotificados",
    "probabilidadeRtMaiorQueUm", "taxaIncidenciaPor100k", "estimativaRt", "populacaoEstimada",
    "temperaturaMinMedia", "temperaturaMedMedia", "temperaturaMaxMedia",
    "umidadeMinMedia", "umidadeMedMedia", "umidadeMaxMedia",
    "indicadorReceptividadeClimatica", "evidenciaTransmissaoSustentada"
]
# Criar DataFrame com as colunas utilizadas
df_resumo = df_filtrado[colunas_utilizadas]
# Exibir a tabela de resumo
st.write(df_resumo.rename(columns=labels_columns))
