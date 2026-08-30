import pandas as pd
import numpy as np
import sqlite3

def criar_banco_e_tabela():
    
    conexao = sqlite3.connect('varejo.db')
    cursor = conexao.cursor()
    
    query_criacao_tabela = '''
    CREATE TABLE IF NOT EXISTS tb_vendas_consolidada (
        ID_VENDA TEXT,
        DATA TEXT,
        PRODUTO_ID TEXT,
        QTD INTEGER,
        VALOR_UNIT REAL,
        CANAL_VENDA TEXT,
        TOTAL_VENDA REAL
    )
    '''
    cursor.execute(query_criacao_tabela)
    
    conexao.commit()
    
    print("Fase 1 Concluída: Banco 'varejo.db' e tabela criados com sucesso!")
    
    return conexao


def limpar_e_tratar(conexao):
    print("Iniciando a extração e tratamento dos dados...")
    df_vendas_lojas = pd.read_csv('data/vendas_lojas.csv')
    df_vendas_web = pd.read_json('data/vendas_web.json')

    df_vendas_lojas.columns = (df_vendas_lojas.columns.str.strip().str.upper())
    df_vendas_lojas['PRODUTO_ID'] = df_vendas_lojas['PRODUTO_ID'].str.strip().str.upper()
    df_vendas_lojas['VALOR_UNIT'] = df_vendas_lojas['VALOR_UNIT'].replace(['NaN', 'nan', 'NAN'], np.nan)
    
    df_vendas_lojas = df_vendas_lojas[df_vendas_lojas['QTD'] > 0]

    df_vendas_web = df_vendas_web.rename(columns={
        'cod_transacao': 'ID_VENDA',
        'data_registro': 'DATA',
        'id_prod' : 'PRODUTO_ID',
        'quant' : 'QTD',
        'preco_unitario' : 'VALOR_UNIT'
    })

    df_vendas_web['PRODUTO_ID'] = df_vendas_web['PRODUTO_ID'].str.strip().str.upper()
    df_vendas_web['VALOR_UNIT'] = df_vendas_web['VALOR_UNIT'].replace(['NaN', 'nan', 'NAN'], np.nan)
    
    df_vendas_web = df_vendas_web[df_vendas_web['QTD'] > 0]


    df_produtos = pd.concat([
        df_vendas_lojas[['PRODUTO_ID', 'VALOR_UNIT']],
        df_vendas_web[['PRODUTO_ID', 'VALOR_UNIT']]
    ]).drop_duplicates(subset=['PRODUTO_ID'])

    cadastro_produtos = pd.Series(df_produtos['VALOR_UNIT'].values, index=df_produtos['PRODUTO_ID']).to_dict()


    df_vendas_lojas['VALOR_UNIT'] = df_vendas_lojas['VALOR_UNIT'].fillna(
        df_vendas_lojas['PRODUTO_ID'].map(cadastro_produtos)
    )

    df_vendas_web['VALOR_UNIT'] = df_vendas_web['VALOR_UNIT'].fillna(
        df_vendas_web['PRODUTO_ID'].map(cadastro_produtos)
    )

    
    df_vendas_lojas['CANAL_VENDA'] = 'Loja Física'
    df_vendas_web['CANAL_VENDA'] = 'E-commerce'

    df_vendas_lojas['DATA'] = pd.to_datetime(
        df_vendas_lojas['DATA'],
        format='mixed',
        dayfirst=True,
        errors='coerce'
    )

    df_vendas_web['DATA'] = pd.to_datetime(
        df_vendas_web['DATA'],
        format='mixed',
        dayfirst=True,
        errors='coerce'
    )

    df_vendas_lojas['DATA'] = df_vendas_lojas['DATA'].dt.strftime('%Y-%m-%d')
    df_vendas_web['DATA'] = df_vendas_web['DATA'].dt.strftime('%Y-%m-%d')

    vendas_consolidadas = pd.concat([df_vendas_lojas,df_vendas_web], ignore_index= True)

    vendas_consolidadas['TOTAL_VENDA'] = vendas_consolidadas['QTD'] * vendas_consolidadas['VALOR_UNIT']

    vendas_consolidadas = vendas_consolidadas.dropna(subset=['VALOR_UNIT'])

    vendas_consolidadas.to_sql(name='tb_vendas_consolidada', con=conexao, if_exists='replace', index=False)

    return vendas_consolidadas

if __name__ == '__main__':

    minha_conexao = criar_banco_e_tabela() 
    dados_prontos = limpar_e_tratar(minha_conexao)
    