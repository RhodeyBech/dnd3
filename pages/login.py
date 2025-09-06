# Rodrigo Bechara 23/08/2025
# Descrição: Tela de login para o sistema
import streamlit        as st

# Import local pasta anterior
import sys
sys.path.append("...")
import functions        as fn

# Oculta menu padrão de navegação do Streamlit
st.markdown("""
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# Identifica se o usuário está logado
if st.session_state.get("is_logged", False):
    st.switch_page("pages/home.py")

# Configuração da página
st.set_page_config(
    page_title="Archivist"
    ,page_icon=""
    ,layout="centered"
)

# ajusta barra lateral
fn.load_sidebar()

# Título
st.title("Archivist")
st.subheader("Sistema pra gente jogar D&D 3.5")

# Define página ativa
st.session_state["active_page"] = "login"

# Formulário de Entrada
with st.form("login_form"):
    st.subheader("Entrar")

    username = st.text_input(label="Usuário", value=st.session_state.get("username", ""), max_chars=60)
    password = st.text_input(label="Senha", type="password")
    placeholder_login = st.empty()

    col1, col2, col3 = st.columns([1, 2, 3])
    with col1:
        # Entrada
        if st.form_submit_button("Entrar", use_container_width=True):
            placeholder_login.warning("Entrando...")
            if fn.check_login(username, password):
                st.switch_page("pages/home.py")
            else:
                placeholder_login.error("Usuário e/ou senha inválidos.")
                st.session_state["is_logged"] = False