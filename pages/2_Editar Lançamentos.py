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


# st.session_state.pop('df_filtro')

if ca.esta_logado():
    teste = ut.controle_paginas('editar')
    if not teste:
        ut.apagar_sessao('df_filtro')
        ut.apagar_sessao('retorno')

    if 'retorno' in st.session_state:
        if st.session_state['retorno'] == 'editar_sucesso':
            st.success('Registro atualizado sucesso!', icon='✅')
            st.session_state['retorno'] = ''

    

    st.title('Editar dados:')
    st.divider()
    st.write('Escolha o período:')
    df=ut.recebe_dados()
    # st.dataframe(df)
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.sort_values(by=['Tipo', 'Data'], ascending=True)
    mes_selecionado = st.selectbox('Mês:', list(ut.meses.keys()))
    ano_selecionado = st.selectbox('Ano', df['Data'].dt.year.unique())
    filtrar = st.button('Filtrar')

    if filtrar:
        df_filtro = df[(df['Data'].dt.month == ut.meses[mes_selecionado]) & (df['Data'].dt.year == ano_selecionado)]
        df_filtro['Data'] = df_filtro['Data'].dt.strftime("%d/%m/%Y")
        df_filtro['Valor'] = df_filtro['Valor'].apply(lambda x: f'{x:,.2f}'.replace('.',','))
        st.session_state['df_filtro'] = df_filtro

    if 'df_filtro' in st.session_state:
    
        # Daqui pra baixo, testando colocar tudo no if
        df_filtro = st.session_state['df_filtro']
        st.dataframe(df_filtro)
        st.divider()
        index = st.selectbox("Selecione o número do registro para editar", df_filtro.index)
        registro_selecionado = df_filtro.loc[index]
        # st.write(f"Registro selecionado ({index}):")
        # st.write(registro_selecionado)
        ID = registro_selecionado['ID']
        data = dt.datetime.strptime(registro_selecionado['Data'], "%d/%m/%Y").date()
        data = st.date_input("Data: ", format="DD/MM/YYYY",  value=data)
        descricao = st.text_input("Descrição", registro_selecionado['Descrição'])
        if registro_selecionado['Tipo'] == "Entrada":
            op_tipo = 1
        else:
            op_tipo = 0
        tipo = st.radio("Tipo: ", ['Saída', 'Entrada'], index=op_tipo)
        valor = registro_selecionado['Valor'].replace(',','.')
        valor = st.number_input("Valor: ", value=float(valor))
        btn_gravar = st.button('Gravar', on_click=ut.validar_dados, args=[data, tipo, descricao, valor])
        if btn_gravar:
            if st.session_state['sucesso']:
                df_novo = ut.recebe_dados()
                indices = df_novo.index[df_novo['ID'] == ID].tolist()
                # st.write(indices)
                if len(indices) == 1:
                    indice = indices[0]
                    df_novo.loc[indice, 'Data'] = data
                    df_novo.loc[indice, 'Tipo'] = tipo
                    df_novo.loc[indice, 'Descrição'] = descricao
                    df_novo.loc[indice, 'Valor'] = valor
                    ut.salvar_arquivo_bkp(df_novo)
                    df_novo = ut.recebe_dados()
                    st.session_state.pop('df_filtro')
                    st.session_state['retorno'] = 'editar_sucesso'
                    st.rerun()
                elif len(indices) > 1:
                    st.error('Registro duplicado. Contate o administrador do sistema!', icon='❌')
                else:
                    st.error('Registro não localizado!', icon='❌')
            else:
                st.error('Houve algum problema no cadastro!', icon='❌')