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
    st.title("Prestação de Contas")
    st.divider()
    df = ut.recebe_dados()
    st.dataframe(df)