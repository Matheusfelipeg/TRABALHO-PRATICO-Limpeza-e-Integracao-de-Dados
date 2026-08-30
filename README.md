# 🛒 ETL e Análise de Vendas Multicanal (Varejo) - Trabalho Prático

Este projeto foi desenvolvido com o objetivo de criar um pipeline completo de ETL (Extract, Transform and Load) utilizando Python, Pandas e SQLite para consolidar, limpar e analisar dados de vendas provenientes de diferentes canais de um varejo. A partir da união de dados de lojas físicas e e-commerce, o projeto estrutura as informações e gera métricas financeiras essenciais para a tomada de decisão.

## 📄 Estrutura do Repositório

* **`ingestion_pipeline.py`**: Script executável contendo toda a lógica de extração, tratamento e carga no banco de dados.
* **`analise_vendas.ipynb`**: Jupyter Notebook com as consultas SQL, cálculo de métricas de negócio e visualizações gráficas.
* **`varejo.db`**: Banco de dados relacional SQLite gerado automaticamente com os dados consolidados.
* **`histograma_vendas.png`**: Gráfico gerado a partir da distribuição/evolução das vendas.
* **`/data/`**: Diretório contendo os dados brutos (`vendas_lojas.csv`, `vendas_web.json`) e os exportados (`vendas_ecommerce_limpo.json`).

## ➕ Contexto

No cenário atual do varejo, empresas operam com múltiplos canais de venda (físico e online) que frequentemente geram dados em formatos distintos (CSV, JSON, etc.) e com diferentes padrões de nomenclatura. A falta de integridade referencial — como produtos registrados sem valor unitário — e o registro de devoluções podem corromper o cálculo do faturamento real.

Este projeto resolve esse problema unificando as bases de Lojas Físicas e E-commerce. O fluxo de ETL foi desenhado para tratar anomalias, cruzar bases para preencher informações faltantes, descartar transações inválidas e disponibilizar os dados limpos em um banco relacional, permitindo a extração rápida de indicadores de performance comercial.

## ⚙️ Processo ETL

O projeto foi estruturado nas seguintes etapas:

**1. Extração (Extract)**
* Importação dos dados de vendas de lojas físicas via arquivo `.csv`.
* Importação dos dados de vendas online via arquivo `.json`.

**2. Transformação (Transform)**
* Padronização de nomes de colunas e identificadores de produtos.
* Mapeamento cruzado (dicionário de produtos) para preenchimento de Valores Unitários ausentes (`NaN`).
* Filtragem de dados financeiros reais, removendo quantidades negativas (devoluções/estornos).
* Criação de novas métricas calculadas, como o `TOTAL_VENDA`.
* Formatação e padronização de datas para o formato `YYYY-MM-DD`.
* Remoção definitiva de registros inconsistentes (produtos fantasmas) para garantir a integridade referencial.

**3. Carga (Load)**
* Inserção dos dados estruturados em uma tabela consolidada (`tb_vendas_consolidada`) no banco de dados **SQLite** (`varejo.db`).
* Exportação de recortes específicos de dados limpos em formato JSON para integrações futuras.

## 📊 Análises Realizadas

Com os dados consolidados no banco, as seguintes métricas e visualizações foram desenvolvidas:
* **Faturamento Total:** Cálculo do volume financeiro bruto de vendas válidas.
* **Ticket Médio:** Razão entre o faturamento total e a quantidade de itens vendidos.
* **Desempenho por Canal:** Comparativo financeiro direto entre vendas no E-commerce e nas Lojas Físicas.
* **Distribuição Visual:** Geração de gráficos (Histograma/Barras) para análise da frequência e volume de vendas.

## 🚀 Tecnologias e Ferramentas

* 🐍 **Python** (Linguagem principal)
* 📄 **Pandas** & **NumPy** (Manipulação e transformação de dados)
* 🗄️ **SQLite** (Armazenamento relacional e consultas SQL)
* 📊 **Matplotlib** (Visualização de dados)
* 📓 **Jupyter Notebook** (Análise interativa)
* 💻 **VS Code** & **Git/GitHub** (Ambiente de desenvolvimento e versionamento)
