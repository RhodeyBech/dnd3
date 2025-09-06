import streamlit        as st

# Configura a página
st.set_page_config(
    page_title="Archivist"
    ,page_icon=""
    ,layout="centered"
)

if "is_logged" not in st.session_state:
    st.session_state["is_logged"] = False

# Carrega a página inicial
st.switch_page("pages/login.py")