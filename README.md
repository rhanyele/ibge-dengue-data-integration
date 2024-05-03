# Projeto de Integração de Dados do IBGE e InfoDengue

Este projeto consiste em uma aplicação Python para extrair dados de municípios brasileiros do Instituto Brasileiro de Geografia e Estatística ([IBGE](https://www.ibge.gov.br/)) e dados de casos de dengue do sistema [InfoDengue](https://info.dengue.mat.br/). Os dados são então transformados e carregados em um banco de dados PostgreSQL para análise posterior e criação de um dashboard. Foi utilizado o Streamlit para criar um dashboard interativo para monitoramento epidemiológico no Brasil.

![untitled (1)](https://github.com/rhanyele/ibge-dengue-data-integration/assets/10997593/2aef0d52-2756-451d-852f-7f931730ba5b)

### Documentação das APIS
- [Municipios IBGE](https://servicodados.ibge.gov.br/api/docs/localidades#api-bq)
- [InfoDengue](https://info.dengue.mat.br/services/api)

## Estrutura do projeto
```bash
- ETL
    - extract.py
    - load.py
    - transform.py
- app.py
- dashboard.py
```

## Funcionalidades
- **Extrair dados do IBGE:** Busca dados de municípios brasileiros na API do IBGE.
- **Extrair dados de dengue:** Busca dados de casos de dengue para cada município na API do InfoDengue.
- **Transformar dados:** Transforma os dados brutos em estruturas de dados adequadas para análise.
- **Carregar dados:** Carrega os dados transformados em um banco de dados PostgreSQL.
- **Pipeline:** Faz o processo de Extração, Transformação e Carga dos dados (ETL).
- **Dashboard:** Visualização dos dados epidemiológicos de dengue.

## Requisitos
- Python
- Poetry
- Pandas
- SQLAlchemy
- PostgreSQL
- Streamlit
- Plotly

## Instalação
1. Clone este repositório:
   ```bash
   git clone https://github.com/rhanyele/ibge-dengue-data-integration.git
   ```

2. Acesse o diretório do projeto:
   ```bash
   cd ibge-dengue-data-integration
   ```

3. Instale as dependências usando Poetry:
   ```bash
   poetry install
   ```

4. Configure as variáveis de ambiente no arquivo `.env` com as informações do seu banco de dados PostgreSQL:
   ```
   DB_HOST=seu_host
   DB_PORT=sua_porta
   DB_NAME=seu_banco_de_dados
   DB_USER=seu_usuario
   DB_PASS=sua_senha
   ```

## Uso
Execute o pipeline ETL:
```bash
poetry run python app.py
```

Execute o dashboard:
```bash
poetry run streamlit run dashboard.py
```
## Demonstração do dashboard
![dashboard](https://github.com/rhanyele/ibge-dengue-data-integration/assets/10997593/b11a54e7-ad5b-46f0-939c-af0a10e4945e)

## Contribuição
Sinta-se à vontade para contribuir com novos recursos, correções de bugs ou melhorias de desempenho. Basta abrir uma issue ou enviar um pull request!

## Autor
[Rhanyele Teixeira Nunes Marinho](https://github.com/rhanyele)

## Licença
Este projeto está licenciado sob a [MIT License](LICENSE).
