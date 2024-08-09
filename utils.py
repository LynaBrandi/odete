import streamlit as st
import pandas as pd
import datetime as dt
import os
import ctrl_acesso as ca


meses = {
    'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4,
    'Maio': 5, 'Junho': 6, 'Julho': 7, 'Agosto': 8,
    'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12
}


ARQUIVO = 'controle_novo.csv'


def apagar_sessao(chave):
    if chave in st.session_state:
        st.session_state.pop(chave)


def recebe_dados():
    dados = pd.read_csv(ARQUIVO)
    return pd.DataFrame(dados)


def validar_dados(data, tipo, descricao, valor):
    if descricao and data <= dt.date.today():
        st.session_state['sucesso'] = True
    else:
        st.session_state['sucesso'] = False


def salvar_arquivo_bkp(tabela_dados):
    agora = dt.datetime.now()
    nome_backup = f'{ARQUIVO.rstrip(".csv")}_{agora.strftime("%Y%m%d_%H%M%S_%f")}.csv'
    os.rename(f'{ARQUIVO}', nome_backup)
    tabela_dados.to_csv(f'{ARQUIVO}', index=False)


def relatorio():
    if ca.esta_logado():
        st.title('Relatórios')
        st.divider()
        st.write('Escolha o período:')
        dados = pd.read_csv('controle.csv')
        df=pd.DataFrame(dados)
        df['Data'] = pd.to_datetime(df['Data'])
        mes_selecionado = st.selectbox('Mês:', list(meses.keys()))
        ano_selecionado = st.selectbox('Ano', df['Data'].dt.year.unique())
        gerar_relatorio = st.button('Gerar Relatório')
        st.write(f'Mês: {mes_selecionado} - Ano: {ano_selecionado}')
        if gerar_relatorio:
            df_relatorio = df[(df['Data'].dt.month == meses[mes_selecionado]) & (df['Data'].dt.year == ano_selecionado)]
            df_entradas = df_relatorio[(df_relatorio['Tipo'] == 'Entrada')]
            df_saidas = df_relatorio[(df_relatorio['Tipo'] == 'Saída')]
            total_entradas = df_entradas['Valor'].sum()
            total_saidas = df_saidas['Valor'].sum()
            saldo = total_entradas - total_saidas
            df_relatorio['Dataf'] = df_relatorio['Data'].dt.strftime("%d/%m/%Y")
            df_relatorio['Valor'] = df_relatorio['Valor'].apply(lambda x: f'{x:,.2f}'.replace('.',','))
            colunas_selecionadas = ["Dataf", "Tipo", "Descrição", "Valor"]
            #st.write(colunas_selecionadas)
            st.dataframe(df_relatorio[colunas_selecionadas])
            st.write(f'Entradas: R$ {total_entradas}')
            st.write(f'Saídas: R$ {total_saidas}')


# Função para saber se o usuário acabou de entrar na página, para ajudar no controle cdas variáveis de sessão
# Se retornar 0, o usuário acabou de entrar na página.
# Se retornar 1, o usuário executou uma operação, mas permanece na mesma página
def controle_paginas(pagina):
    if 'pagina_anterior' not in st.session_state:
        st.session_state['pagina_anterior'] = ''
    if 'pagina_atual' not in st.session_state:
        st.session_state['pagina_atual'] = pagina
        return 0
    st.session_state['pagina_anterior'] = st.session_state['pagina_atual']
    st.session_state['pagina_atual'] = pagina
    if st.session_state['pagina_anterior'] == st.session_state['pagina_atual']:
        return 1
    else:
        return 0
    