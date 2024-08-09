import streamlit as st
import pandas as pd
import datetime as dt
import os
import ctrl_acesso as ca
import utils as ut

st.set_page_config(
    page_title='Prestação de Contas',
    page_icon='💲',
    layout='wide'
)

teste = ut.controle_paginas('novo')

if ca.esta_logado():
    st.title('Novo Lançamento:')
    st.divider()
    df = ut.recebe_dados()
    df_ultimos = df.tail(2)
    df_ultimos['Data'] = pd.to_datetime(df_ultimos['Data'])
    df_ultimos['Data'] = df_ultimos['Data'].dt.strftime("%d/%m/%Y")
    df_ultimos['Valor'] = df_ultimos['Valor'].apply(lambda x: f'{x:,.2f}'.replace('.',','))
    colunas = ['Data', 'Tipo', 'Descrição', 'Valor']
    # st.write(f'Novo ID: {novo_id}')
    st.dataframe(df_ultimos[colunas])
    data = st.date_input("Data: ", format="DD/MM/YYYY")
    tipo = st.radio("Tipo: ", ['Saída', 'Entrada'])
    descricao = st.text_input("Descrição: ")
    valor = st.number_input("Valor: ")
    btn_cadastrar = st.button('Cadastrar', on_click=ut.validar_dados, args=[data, tipo, descricao, valor])
    if btn_cadastrar:
        if st.session_state['sucesso']:
            novo_id = int(df.iloc[-1]['ID'])+1
            with open(ut.ARQUIVO, 'a', encoding='utf-8') as file:
                file.write(f'{novo_id},{data},{tipo},{descricao},{valor}\n')
            st.success('Lançamento cadastrado com sucesso!', icon='✅')
            st.rerun()
        else:
            st.error('Houve algum problema no cadastro!', icon='❌')