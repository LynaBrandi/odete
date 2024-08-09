import streamlit as st
# ### INÍCIO CONTROLE DE ACESSO ### #
# Dicionário de usuários e senhas
users = {
    "admin": "1234",
    "tania": "1234"
}

# Função para verificar o login
def check_login(username, password):
    if username in users and users[username] == password:
        return True
    return False

# Interface de login
def login():
    st.title("Login")
    username = st.text_input("Nome de usuário")
    password = st.text_input("Senha", type="password")
    btlogin = st.button("Login")
    if btlogin:
        if check_login(username, password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.error("Nome de usuário ou senha incorretos")

# Verifica se está logado
def esta_logado():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
    if not st.session_state["logged_in"]:
        login()
    else:
        return True
    return False

def logout():
    st.session_state['logged_in'] = False
    st.session_state["username"] = ''

# ### FIM CONTROLE DE ACESSO ### #
