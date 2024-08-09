import streamlit as st
import pandas as pd

# Dados iniciais
data = {
    'Nome': ['Alice', 'Bob', 'Charlie'],
    'Idade': [25, 30, 35],
    'Cidade': ['New York', 'Los Angeles', 'Chicago']
}

# Transformando os dados em um DataFrame
df = pd.DataFrame(data)

# Função para exibir o DataFrame
def display_dataframe(df):
    st.dataframe(df)

# Função para editar um registro
def edit_record(index):
    with st.form(key=f'edit_form_{index}'):
        nome = st.text_input('Nome', value=df.loc[index, 'Nome'])
        idade = st.number_input('Idade', value=df.loc[index, 'Idade'], step=1)
        cidade = st.text_input('Cidade', value=df.loc[index, 'Cidade'])
        submit_button = st.form_submit_button(label='Salvar')
        
        if submit_button:
            df.at[index, 'Nome'] = nome
            df.at[index, 'Idade'] = idade
            df.at[index, 'Cidade'] = cidade
            st.success('Registro atualizado com sucesso!')
            st.rerun()

# Título da aplicação
st.title('Editar Registros do DataFrame')

# Exibir o DataFrame
display_dataframe(df)

# Adicionar botões para editar registros
for i in range(len(df)):
    if st.button(f'Editar {i}', key=f'edit_button_{i}'):
        edit_record(i)

# Exibir o DataFrame atualizado
st.subheader('DataFrame Atualizado')
display_dataframe(df)