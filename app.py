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

ut.controle_paginas('app')

if ca.esta_logado():
    st.title("Prestação de Contas")
    st.divider()
    df = ut.recebe_dados()
    df_ultimos = df.tail(15)
    df_ultimos['Data'] = pd.to_datetime(df_ultimos['Data'])
    df_ultimos['Data'] = df_ultimos['Data'].dt.strftime("%d/%m/%Y")
    df_ultimos['Valor'] = df_ultimos['Valor'].apply(lambda x: f'{x:,.2f}'.replace('.',','))
    colunas = ['Data', 'Tipo', 'Descrição', 'Valor']
    st.dataframe(df_ultimos[colunas])

