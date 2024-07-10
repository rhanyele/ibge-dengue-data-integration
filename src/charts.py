import streamlit as st
import plotly.express as px
from load_app import labels_columns

def grafico1(df_filtrado):
    # Gráfico 1: Comparação entre Casos Estimados e Casos Notificados por Semana
    st.subheader('Comparação entre Casos Estimados e Casos Notificados por Semana')
    st.caption('Número de casos notificados, número de casos estimados usando o modelo de nowcasting e intervalo de credibilidade de 95% do número de casos estimados.')
    fig1 = px.line(df_filtrado, x='semanaEpidemiologica', y=['casosEstimados', 'casosNotificados'], labels=labels_columns)
    fig1.add_scatter(x=df_filtrado['semanaEpidemiologica'], y=df_filtrado['casosEstimadosMin'], 
                    mode='lines', line=dict(dash='dash'), name='casosEstimadosMin')
    fig1.add_scatter(x=df_filtrado['semanaEpidemiologica'], y=df_filtrado['casosEstimadosMax'], 
                    mode='lines', line=dict(dash='dash'), name='casosEstimadosMax')
    st.plotly_chart(fig1)

def grafico2(df_filtrado):
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

def grafico3(df_filtrado):
    # Gráfico 3: Taxa de Incidência por 100.000 Habitantes por Semana
    st.subheader('Taxa de Incidência por 100.000 Habitantes por Semana')
    st.caption('Taxa de incidência estimada por 100.000 habitantes')
    fig3 = px.line(df_filtrado, x='semanaEpidemiologica', y='taxaIncidenciaPor100k', text='taxaIncidenciaPor100k', labels=labels_columns)
    # Adicionar rótulos de valores aos pontos de dados
    fig3.update_traces(textposition='top right')
    fig3.update_traces(marker=dict(color='orange'), selector=dict(type='scatter', mode='markers', y='probabilidadeRtMaiorQueUm', y0=0.95))
    # Configurações de layout
    fig3.update_layout(yaxis_tickvals=[])
    st.plotly_chart(fig3)

def grafico4(df_filtrado):
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

def grafico5(data, ano_filtrado, estado_filtrado):
        # Gráfico 5: Mapa de Calor: Indicador Receptividade Climática dos municípios do estado
    st.subheader('Indicador Receptividade Climática')
    st.caption('Legenda:\n0 = desfavorável,\n1 = favorável,\n2 = favorável nesta semana e na semana passada,\n3 = favorável por pelo menos três semanas (suficiente para completar um ciclo de transmissão).')
    df_ano_filtrado = data[data['ano'] == ano_filtrado]
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

def grafico6(data, municipio_filtrado):
    # Gráfico 6: Casos Acumulados por Ano (considerando o filtro de município)
    st.subheader('Casos Acumulados por Ano no Município')
    st.caption('Número acumulado de casos notificados no ano.')
    # Pega o DataFrame principal e filtra o município
    df_filtrado_municipio = data[(data['municipioNome'] == municipio_filtrado)]
    # Soma todos os casos notificados do ano 
    df_casos_acumulados_por_ano = df_filtrado_municipio.groupby('ano')['casosNotificados'].sum().reset_index()
    # Montando o gráfico de barras
    fig6 = px.bar(df_casos_acumulados_por_ano, x='ano', y='casosNotificados', text='casosNotificados', labels=labels_columns)
    fig6.update_xaxes(tickformat="d")  # Definir a escala do eixo x como inteiros
    fig6.update_layout(yaxis_tickvals=[])
    st.plotly_chart(fig6)

def tabela_resumo(df_filtrado):
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