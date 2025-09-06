# Rodrigo Bechara 14/07/2025
# Descrição: Tela de home para o sistema
import streamlit            as st
import sqlalchemy           as sa
import pandas               as pd
import time
import json

# Import local pasta anterior
import sys
sys.path.append("...")
import functions            as fn

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
    # st.switch_page("pages/login")

# Ajusta cabeçalho da página
fn.hidden_header()

# Configuração da página
st.set_page_config(
    page_title="Nexus"
    ,page_icon="https://www.csg.com.br/build/assets/favicon-c752c7b3.png"
    ,layout="wide"
)

# Define página ativa
st.session_state["active_page"] = "home"

# Carrega a barra lateral
fn.load_sidebar()

# Título
st.subheader("Início")

# Cria colunas
col1, col2, col3 = st.columns([4, 2, 4])

with col1:
    # Tela após login bem-sucedido
    st.markdown(f"##### Bem-vindo(a) {st.session_state.get("username").title().replace(".", " ")}.")
# with col2:
#     st.write(f"Tema:")

# Cria colunas
col4, col5, col6, col7 = st.columns([1, 1, 2, 6])

with col4:
    if st.button("Alterar Senha", use_container_width=True):
        st.session_state["home_menu"] = "change_password"
with col5:
    if st.button("Sair", use_container_width=True):
        st.session_state["home_menu"] = "logout"

# with col6:
#     # Seleção de Tema
#     theme_options = {
#         "Padrão": "Padrão",
#         "Claro": "Claro",
#         "Escuro": "Escuro",
#         "CSG": "CSG"
#     }
#     st.markdown("""
#         <style>
#             div[data-baseweb="select"] > div {
#                 margin-top: -44px;
#             }
#         </style>
#     """, unsafe_allow_html=True)
#     theme = st.selectbox("", options=list(theme_options.keys()), index=list(theme_options.values()).index(st.session_state.get("theme")))
#     st.session_state["theme"] = theme
#     # Obtém conexão ao banco
#     engine = fn.get_pd_connection()
#     with engine.begin() as cn:
#         query = sa.text("""
#             UPDATE Nexus.auth.Users
#                 SET
#                     Theme = :theme
#                 WHERE
#                     Username = :username
#         """)
#         result = cn.execute(query, {
#             "theme": st.session_state.get("theme")
#             ,"username": st.session_state.get("username")
#         })
#         cn.commit()
#         cn.close()

#     fn.alter_theme()

# Obtém opção
option = st.session_state.get("home_menu")

# Sair
if option == "logout":
    del st.session_state["home_menu"]
    del st.session_state["is_logged"]
    st.switch_page("pages/login.py")
    # st.switch_page("pages/login")

# Alterar Senha
if option == "change_password":
    with st.form("change_password", width=500):
        st.text_input(label="Usuário", value=st.session_state["username"], disabled=True)
        old_password = st.text_input(label="Senha Atual", type="password")
        new_password_1 = st.text_input(label="Nova Senha", type="password")
        new_password_2 = st.text_input(label="Confirmar Nova Senha", type="password")

        # Cria colunas
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            bt_confirm = st.form_submit_button("Confirmar", use_container_width=True)
        with col2:
            bt_cancel = st.form_submit_button("Cancelar", use_container_width=True)

        # Botão Confirmar
        if bt_confirm:
            if fn.check_login(st.session_state["username"], old_password):
                if new_password_1 == new_password_2:
                    try:
                        # Obtém conexão ao banco
                        engine = fn.get_pd_connection()

                        with engine.begin() as cn:
                            query = sa.text("""
                                UPDATE Nexus.auth.Users
                                    SET
                                        PasswordHash = :password
                                    WHERE
                                        Username = :username
                            """)
                            result = cn.execute(query, {
                                "password": fn.hash_password(new_password_1)
                                ,"username": st.session_state.get("username")
                            })
                            cn.commit()
                            cn.close()

                            if result.rowcount > 0:
                                st.success("Senha alterada com sucesso.")
                                del st.session_state["home_menu"]
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Erro ao alterar senha.")

                    except Exception as e:
                        st.error(f"Erro ao alterar senha: {e}")
                else:
                    st.error("Nova senha não confere.")
            else:
                st.error("Senha atual incorreta.")

        # Cancelar
        elif bt_cancel:
            del st.session_state["home_menu"]
            st.rerun()


col8, col9, col10 = st.columns([4, 4, 12])
with col8:
    fn.shift_top(8)
    st.subheader("Acesso Rápido")
    # Intranet
    st.markdown("""
        <a href="https://webapp395138.ip-97-107-134-242.cloudezapp.io" target="_blank" style="display: inline-flex; align-items: center; text-decoration: none;">
        <img src="https://www.csg.com.br/build/assets/favicon-c752c7b3.png" width="16" style="margin-right: 8px;">
        Intranet - CSG
        </a>
    """, unsafe_allow_html=True)
    st.markdown("\n")
    # Zendesk
    st.markdown("""
        <a href="https://csg-concessionaria.zendesk.com/hc/pt-br" target="_blank" style="display: inline-flex; align-items: center; text-decoration: none;">
        <img src="https://csg-concessionaria.zendesk.com/hc/theming_assets/01JKTWRF5DWYEYT4E2MXDNWWCX" width="16" style="margin-right: 8px;">
        Zendesk - Central de Ajuda
        </a>
    """, unsafe_allow_html=True)
    st.markdown("\n")
    # Senior
    st.markdown("""
        <a href="https://web02s1p.seniorcloud.com.br:31051/gestaoponto-frontend/login" target="_blank" style="display: inline-flex; align-items: center; text-decoration: none;">
        <img src="https://web02s1p.seniorcloud.com.br:31051/gestaoponto-frontend/favicon.png" width="16" style="margin-right: 8px;">
        Senior
        </a>
    """, unsafe_allow_html=True)
    st.markdown("\n")
    # Scoreplan
    st.markdown("""
        <a href="https://app.scoreplan.com.br/login" target="_blank" style="display: inline-flex; align-items: center; text-decoration: none;">
        <img src="https://app.scoreplan.com.br/mask-icon.png" width="16" style="margin-right: 8px;">
        Scoreplan
        </a>
    """, unsafe_allow_html=True)
    st.markdown("\n")
    # kapsch
    st.markdown("""
        <a href="https://front.operian.csg.com.br" target="_blank" style="display: inline-flex; align-items: center; text-decoration: none;">
        <img src="https://logodix.com/logo/2016268.png" width="16" style="margin-right: 8px;">
        kapsch - Operacional
        </a>
    """, unsafe_allow_html=True)
    st.markdown("\n")
    # InteropFlex
    st.markdown("""
        <a href="https://app.ifx.operian.csg.com.br/#/login?returnUrl=%2Fhome" target="_blank" style="display: inline-flex; align-items: center; text-decoration: none;">
        <img src="https://logodix.com/logo/2016268.png" width="16" style="margin-right: 8px;">
        kapsch - InteropFlex
        </a>
    """, unsafe_allow_html=True)
    st.markdown("\n")
    # Attri
    st.markdown("""
        <a href="https://painel.freeflow.csg.com.br/login" target="_blank" style="display: inline-flex; align-items: center; text-decoration: none;">
        <img src="https://painel.freeflow.csg.com.br/favicon.ico" width="16" style="margin-right: 8px;">
        Attri - Painel Administrativo
        </a>
    """, unsafe_allow_html=True)
    st.markdown("\n")
    # Autolist
    st.markdown("""
        <a href="http://10.0.50.101:8080/ConsultaVeiculos" target="_blank" style="display: inline-flex; align-items: center; text-decoration: none;">
        <img src="https://scontent.fpoa2-1.fna.fbcdn.net/v/t39.30808-6/303614908_103085555878187_1574554606710422950_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=6ee11a&_nc_ohc=3q1bHa4el3UQ7kNvwHS8epk&_nc_oc=Adl1bxZDE5GzmLKBE9X3PCrhNQv_xne9aha2mxYaHUodX6d3z5kG4y3Cwz4TThX6q4E&_nc_zt=23&_nc_ht=scontent.fpoa2-1.fna&_nc_gid=Vnglxx20xw3VWTt-juXNzw&oh=00_AfRgf8KpGv_-N3d2k04oV_184WjiprU7xuAy0pHYvlqK3g&oe=6885CA5D" width="16" style="margin-right: 8px;">
        Autolist - Consulta Veículos
        </a>
    """, unsafe_allow_html=True)
    st.markdown("\n")

with col9:
    fn.shift_top(49)
    # ConectCar
    st.markdown("""
        <a href="https://conveniado.conectcar.com/Autenticacao/Autenticar" target="_blank" style="display: inline-flex; align-items: center; text-decoration: none;">
        <img src="https://cdn.conectcar.com/imagens/favicon.ico" width="16" style="margin-right: 8px;">
        ConectCar
        </a>
    """, unsafe_allow_html=True)
    st.markdown("\n")
    # GreenPass
    st.markdown("""
        <a href="https://conveniado.greenpass.com.br/Account/Login" target="_blank" style="display: inline-flex; align-items: center; text-decoration: none;">
        <img src="https://conveniado.greenpass.com.br/img/apple-icon-57x57.png" width="16" style="margin-right: 8px;">
        GreenPass
        </a>
    """, unsafe_allow_html=True)
    st.markdown("\n")
    # Move Mais
    st.markdown("""
        <a href="https://pdcmm.movemais.com/login" target="_blank" style="display: inline-flex; align-items: center; text-decoration: none;">
        <img src="https://pdcmm.movemais.com/favicon.ico" width="16" style="margin-right: 8px;">
        Move Mais
        </a>
    """, unsafe_allow_html=True)
    st.markdown("\n")
    # Sem Parar
    st.markdown("""
        <a href="https://credenciados.semparar.com.br/login" target="_blank" style="display: inline-flex; align-items: center; text-decoration: none;">
        <img src="https://credenciados.semparar.com.br/assets/favicon.png" width="16" style="margin-right: 8px;">
        Sem Parar
        </a>
    """, unsafe_allow_html=True)
    st.markdown("\n")
    # Veloe
    st.markdown("""
        <a href="https://beta-portal-ec.veloe.com.br/portalec-shell-frt/login" target="_blank" style="display: inline-flex; align-items: center; text-decoration: none;">
        <img src="https://beta-portal-ec.veloe.com.br/portalec-shell-frt/favicon.ico" width="16" style="margin-right: 8px;">
        Veloe
        </a>
    """, unsafe_allow_html=True)
    st.markdown("\n")

with col10:
    if st.session_state.get("group_id") ==1:
        df_last_reset_cache_pd = fn.get_last_reset_cache_pd()
        StartDatetime = pd.to_datetime(df_last_reset_cache_pd["StartDatetime"].iloc[0])
        Runtime = df_last_reset_cache_pd["Runtime"].iloc[0]
        Status = df_last_reset_cache_pd["Status"].iloc[0]
        Message = df_last_reset_cache_pd["Message"].iloc[0]
        Message = Message.split(".")[0]
        if Message[-1:] != ".":
            Message = f"{Message}."
        # Mensagem
        fn.shift_top(8)
        st.subheader("Última Limpeza do Banco")
        st.text(f"""
            Início:\t\t\t\t\t\t{StartDatetime.strftime("%d/%m/%Y %H:%M:%S")}
            Tempo de Execução:\t\t{Runtime}
            Status:\t\t\t\t\t\t{Status}
            Mensagem:\t\t\t\t{Message}
        """)