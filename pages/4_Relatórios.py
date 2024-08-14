import streamlit as st
import pandas as pd
import datetime as dt
import os
import ctrl_acesso as ca
import utils as ut
import numpy as np

# st.set_page_config(
#     page_title='Prestação de Contas',
#     page_icon='💲',
#     layout='wide',
#     initial_sidebar_state="collapsed"
# )

st.set_page_config(
    page_title='Prestação de Contas',
    page_icon='💲',
    layout='wide'
)


if ca.esta_logado():
    teste = ut.controle_paginas('relatorios')
    # st.write(teste)
    if not teste:
        ut.apagar_sessao('relatorio')
    if 'relatorio' not in st.session_state:
        st.title('Relatórios')
        st.divider()
        st.write('Escolha o período:')
        df=ut.recebe_dados()
        df['Data'] = pd.to_datetime(df['Data'])
        df = df.sort_values(by=['Tipo', 'Data'], ascending=True)
        periodo_padrao = str(dt.datetime.now().year) + "-" + str(dt.datetime.now().month) + "-" + "01"
        teste = dt.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
        # st.write(teste)
        periodo_padrao = dt.datetime.strptime(periodo_padrao, '%Y-%m-%d') - dt.timedelta(days=1)
        mes_selecionado = st.selectbox('Mês:', list(ut.meses.keys()), index=periodo_padrao.month-1)
        ano_selecionado = st.selectbox('Ano', df['Data'].dt.year.unique(), index=int(np.where(df['Data'].dt.year.unique() == periodo_padrao.year)[0]))
        gerar_relatorio = st.button('Gerar Relatório')
        # st.write(f'Mês: {mes_selecionado} - Ano: {ano_selecionado}')
        if gerar_relatorio:
            st.session_state['relatorio'] = 1
            data_inicial = dt.date(int(ano_selecionado), ut.meses[mes_selecionado], 1)
            df_anterior = df[(df['Data'] < pd.to_datetime(data_inicial))]
            df_entradas = df[(df['Tipo'] == 'Entrada') & (df['Data'].dt.month == ut.meses[mes_selecionado]) & (df['Data'].dt.year == ano_selecionado)]
            df_saidas = df[(df['Tipo'] == 'Saída') & (df['Data'].dt.month == ut.meses[mes_selecionado]) & (df['Data'].dt.year == ano_selecionado)]
            total_entradas = df_entradas['Valor'].sum()
            total_saidas = df_saidas['Valor'].sum()
            saldo_anterior = df_anterior[(df_anterior['Tipo'] == 'Entrada')]['Valor'].sum() - df_anterior[(df_anterior['Tipo'] == 'Saída')]['Valor'].sum()
            saldo = total_entradas - total_saidas
            saldo_final = saldo_anterior  + total_entradas - total_saidas
            df_entradas['Dataf'] = df_entradas['Data'].dt.strftime("%d/%m/%Y")
            df_entradas['Valor'] = df_entradas['Valor'].apply(lambda x: f'{x:,.2f}'.replace('.',','))
            df_saidas['Dataf'] = df_saidas['Data'].dt.strftime("%d/%m/%Y")
            df_saidas['Valor'] = df_saidas['Valor'].apply(lambda x: f'{x:,.2f}'.replace('.',','))
            # st.title('Prestação de contas')
            # st.header(f'Mês: {mes_selecionado} - Ano: {ano_selecionado}')
            # st.subheader('Entradas:')
            # st.table(df_entradas[['Dataf', 'Descrição', 'Valor']])
            # st.write(f'Total: R$ ', f'{total_entradas:,.2f}'.replace('.','X').replace(',','.').replace('X',','))
            # st.subheader('Saídas:')
            # st.table(df_saidas[['Dataf', 'Descrição', 'Valor']])
            # st.write(f'Total: R$ ', f'{total_saidas:,.2f}'.replace('.','X').replace(',','.').replace('X',','))
            # st.write(f'Saldo anterior: R$ ', f'{saldo_anterior:,.2f}'.replace('.','X').replace(',','.').replace('X',','))
            # st.write(f'Saldo final: R$ ', f'{saldo_final:,.2f}'.replace('.','X').replace(',','.').replace('X',','))
            codigo_html = '<h3>Prestação de contas</h3>'
            codigo_html += mes_selecionado.capitalize() + " - " + str(ano_selecionado)
            codigo_html += '<h4>Entradas:</h4>'
            codigo_html += '<table><thead><tr><th>Data</th><th>Descrição</th><th>Valor</th></tr></thead><tbody>'
            for indice, linha in df_entradas.iterrows():
                codigo_html += f'<tr><td>{linha["Dataf"]}</td><td>{linha["Descrição"]}</td><td>{linha["Valor"]}</td></tr>'
            codigo_html += '</tr></tbody></table>'
            codigo_html += '<b>Total das Entradas: R$ ' + f'{total_entradas:,.2f}'.replace('.','X').replace(',','.').replace('X',',') + '</b>'
            codigo_html += '<h4>Saídas:</h4>'
            codigo_html += '<table><thead><tr><th>Data</th><th>Descrição</th><th>Valor</th></tr></thead><tbody>'
            for indice, linha in df_saidas.iterrows():
                codigo_html += f'<tr><td>{linha["Dataf"]}</td><td>{linha["Descrição"]}</td><td>{linha["Valor"]}</td></tr>'
            codigo_html += '</tr></tbody></table>'
            codigo_html += '<b>Total das Saídas: R$ ' + f'{total_saidas:,.2f}'.replace('.','X').replace(',','.').replace('X',',') + '</b>'
            codigo_html += '<br/><b>Saldo anterior: R$ ' + f'{saldo_anterior:,.2f}'.replace('.','X').replace(',','.').replace('X',',') + '</b>'
            codigo_html += '<br/><b>Saldo final: R$ ' + f'{saldo_final:,.2f}'.replace('.','X').replace(',','.').replace('X',',') + '</b>'
            codigo_html += '<br/><br/>Relatório emitido em: ' + dt.datetime.now().strftime('%d/%m/%Y às %H:%M:%S') +'.'
            st.session_state['relatorio'] = codigo_html
            st.rerun()
    else:
        st.markdown(st.session_state['relatorio'], unsafe_allow_html=True)