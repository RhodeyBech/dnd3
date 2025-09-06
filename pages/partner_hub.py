# Rodrigo Bechara 22/08/2025
# Página do Hub de Parceiros
import streamlit                as st
import pandas                   as pd
import datetime                 as dt
import json
import sqlalchemy               as sa
import requests

# Import local pasta anterior
import sys
sys.path.append("...")
import functions                as fn

# Oculta menu padrão de navegação do Streamlit
st.markdown("""
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# Altera tema
fn.alter_theme()

# Obtém dados do armazenamento local
# fn.load_data_localstorage()

# Identifica se o usuário está logado
if not st.session_state.get("is_logged", False):
    st.switch_page("pages/login.py")

# Configuração da página
st.set_page_config(
    page_title="Nexus"
    ,page_icon="https://www.csg.com.br/build/assets/favicon-c752c7b3.png"
    ,layout="wide"
)

# Ajusta cabeçalho da página
fn.hidden_header()

# Define página ativa
st.session_state["active_page"] = "partner_hub"

# Carrega a barra lateral
fn.load_sidebar()

# Título
st.subheader("Hub de Parceiros")

# Conexões
engine_pd = fn.get_pd_connection()

def get_partner_hub_get_waze_data_feed():
    url = "https://www.waze.com/row-partnerhub-api/partners/15500500602/waze-feeds/36f2ee75-2917-4876-ae11-ba3e97fdd490?format=1"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return (f"GET Error. Status Code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        return (f"GET Function Internal Error: {e}")

df_partner_hub_get_waze_data_feed = pd.DataFrame()

col1, col2, col3 = st.columns([3, 3, 14])
with col1:
    if st.button("Entrada de Dados do Waze", key="partner_hub_get_waze_data_feed", use_container_width=True):
        st.session_state["partner_hub"] = "partner_hub_get_waze_data_feed"
with col2:
    # fn.shift_top(18)
    csv_partner_hub_get_waze_data_feed = df_partner_hub_get_waze_data_feed.to_csv(sep=";", index=False)
    if "partner_hub_get_waze_data_feed_df" in st.session_state:
        if not st.session_state.get("partner_hub_get_waze_data_feed_df").empty:
            df_partner_hub_get_waze_data_feed = st.session_state.get("partner_hub_get_waze_data_feed_df")
            csv_partner_hub_get_waze_data_feed = df_partner_hub_get_waze_data_feed.to_csv(sep=";", index=False)
    st.download_button(
        label="Baixar CSV"
        ,key="csv_partner_hub_get_waze_data_feed"
        ,data=csv_partner_hub_get_waze_data_feed.encode("utf-8-sig")
        ,file_name="Entrada de Dados do Waze.csv"
        ,mime="text/csv"
        ,use_container_width=True
    )
placeholder_partner_hub = st.empty()

option_partner_hub = st.session_state.get("partner_hub")
if option_partner_hub == "partner_hub_get_waze_data_feed":
    placeholder_partner_hub.warning("Pesquisando...")
    str_partner_hub_get_waze_data_feed = get_partner_hub_get_waze_data_feed()
    # st.text(str_partner_hub_get_waze_data_feed)

    df_partner_hub_get_waze_data_feed = []

    for k, v in str_partner_hub_get_waze_data_feed.items():
        if isinstance(v, list) and len(v) > 0:
            df_temp = pd.json_normalize(v)
            df_temp["__source"] = k
            # st.text(df_temp)
            df_partner_hub_get_waze_data_feed.append(df_temp)

    df_partner_hub_get_waze_data_feed = pd.concat(df_partner_hub_get_waze_data_feed, ignore_index=True)
    st.session_state["partner_hub_get_waze_data_feed_df"] = df_partner_hub_get_waze_data_feed

    placeholder_partner_hub.empty()
    del st.session_state["partner_hub"]
    st.rerun()

if "partner_hub_get_waze_data_feed_df" in st.session_state:
    if not st.session_state.get("partner_hub_get_waze_data_feed_df").empty:
        st.dataframe(st.session_state.get("partner_hub_get_waze_data_feed_df"), height=720)
    else:
        if "partner_hub_get_waze_data_feed_df" in st.session_state:
            del st.session_state["partner_hub_get_waze_data_feed_df"]


        