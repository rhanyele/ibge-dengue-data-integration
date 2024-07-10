import streamlit as st
import logging
from load_app import *
from charts import *

# Configura o logging
logging.basicConfig(level=logging.INFO, filename="logs/.log", filemode='w', format="%(asctime)s - %(levelname)s - %(message)s", encoding="utf-8")

# Função para aplicar filtros
def aplicar_filtros(df, ano_filtrado, regiao_filtrada, estado_filtrado, municipio_filtrado):
    df_filtrado = df[
        (df['ano'] == ano_filtrado) &
        (df['regiaoNome'] == regiao_filtrada) &
        (df['estadoNome'] == estado_filtrado) &
        (df['municipioNome'] == municipio_filtrado)
    ].reset_index(drop=True)
    return df_filtrado

def menu_sidebar(df):
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

    return df_filtrado, municipio_filtrado, estado_filtrado, ano_filtrado

def app_main():

    data = load_data_municipios()

    df_filtrado, municipio_filtrado, estado_filtrado, ano_filtrado = menu_sidebar(data)

    st.subheader(f'Análise do município de {municipio_filtrado}, estado de {estado_filtrado}, ano de {ano_filtrado}.')
    st.caption('Dados extraídos do [InfoDengue](https://info.dengue.mat.br/) e [IBGE](https://www.ibge.gov.br/).')
    st.divider()

    # Restante do código para plotar os gráficos
    grafico1(df_filtrado)

    grafico2(df_filtrado)
    
    grafico3(df_filtrado)

    grafico4(df_filtrado)
    
    grafico5(data, municipio_filtrado, estado_filtrado)

    grafico6(data, municipio_filtrado)

    tabela_resumo(df_filtrado)


            



def main():
    # Título da página
    st.set_page_config(page_title="Meu Dashboard", layout="centered", page_icon="src/img/dengue.png")

    # Título do dashboard
    st.title('Monitoramento Epidemiológico:')

    app_main()
    

if __name__ == '__main__':
    main()
