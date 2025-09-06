# Rodrigo Bechara 14/07/2025
# Descrição: Conslta de placa
import streamlit                as st
import streamlit.components.v1  as stcomp

# Import local pasta anterior
import sys
sys.path.append("...")
# import environ
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
st.session_state["active_page"] = "power_bi"

# Carrega a barra lateral
fn.load_sidebar()

# Título
st.subheader("Power BI")

# Inicializa flags
show_management_tab = False
show_financial_tab = False
show_backoffice_tab = False
show_infrastructure_it_tab = False
show_administrative_it_tab = False
show_communication_tab = False
show_personnel_management_tab = False

# Parâmetros de largura
col_menu_width = 3
col_content_width = 20

# Medidas e valores padrão
power_bi_iframe_height = 800
# power_bi_iframe_width = 1370
# power_bi_iframe_height = "100%"
power_bi_iframe_width = "100%"

# Cria abas
# 1 - Administração
# 2 - Teste de Software
# 3 - Geral
# 4 - Diretoria
# 5 - Backoffice
# 6 - Financeiro
# 7 - TI Infraestrutura
# 8 - TI Administrativa
# 9 - Comunicação
# 10 - Gestão de Pessoas
# Administração, Teste de Software e Diretoria
if st.session_state.get("group_id") in {1, 2, 4}:
    tab_management, tab_backoffice, tab_communication, tab_financial, tab_personnel_management, tab_infrastructure_it, tab_administrative_it = st.tabs([
        "Gerência"
        ,"Backoffice"
        ,"Comunicação"
        ,"Financeiro"
        ,"Gestão de Pessoas"
        ,"TI Infraestrutura"
        ,"TI Administrativa"
    ])
    show_management_tab = True
    show_financial_tab = True
    show_backoffice_tab = True
    show_infrastructure_it_tab = True
    show_administrative_it_tab = True
    show_communication_tab = True
    show_personnel_management_tab = True
# Backoffice
elif st.session_state.get("group_id") == 5:
    tab_backoffice, = st.tabs(["Backoffice"])
    show_backoffice_tab = True
# Financeiro
elif st.session_state.get("group_id") == 6:
    tab_financial, = st.tabs(["Financeiro"])
    show_financial_tab = True
# TI Infraestrutura
elif st.session_state.get("group_id") == 7:
    tab_infrastructure_it, = st.tabs(["TI Infraestrutura"])
    show_infrastructure_it_tab = True
# TI Administrativa
elif st.session_state.get("group_id") == 8:
    tab_administrative_it, = st.tabs(["TI Administrativa"])
    show_infrastructure_it_tab = True
# Comunicação
elif st.session_state.get("group_id") == 9:
    tab_communication, = st.tabs(["Comunicação"])
    show_communication_tab = True
# Gestão de Pessoas
elif st.session_state.get("group_id") == 10:
    tab_personnel_management, = st.tabs(["Gestão de Pessoas"])
    show_personnel_management_tab = True

# Administração, Teste de Software e Diretoria
if show_management_tab:
    with tab_management:
        st.session_state["power_bi_menu_active_tab"] = "tab_management"
        col_menu, col_content = st.columns([col_menu_width, col_content_width])

        with col_menu:
            if st.button("Controle de Infrações", key="management_controle_infracoes", use_container_width=True):
                st.session_state["power_bi_menu"] = "management_controle_infracoes"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiMmNhZmRmNTUtNDU0ZS00NDUzLTk5Y2ItMjUwOWE1YjZkMTZhIiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9"
                st.session_state["power_bi_iframe_name"] = "Controle de Infrações"
            if st.button("Latência de Pagamentos", key="management_latencia_pagamentos", use_container_width=True):
                st.session_state["power_bi_menu"] = "management_latencia_pagamentos"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiODY4OWRiZDUtYWJlZS00ODY4LTgyNzUtYjMxZmRmZTcxMTUwIiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9&pageName=9b3fb541ed007cc88f23"
                st.session_state["power_bi_iframe_name"] = "Latência de Pagamentos"

        with col_content:
            option_management = st.session_state.get("power_bi_menu", "")

            if st.session_state.get("power_bi_menu_active_tab", "") == "tab_management" and option_management in {
                "management_controle_infracoes"
                ,"management_latencia_pagamentos"
            }:
                st.write(st.session_state.get("power_bi_iframe_name"))
                st.markdown(
                    f'''<iframe
                        width="{power_bi_iframe_width}"
                        height="{power_bi_iframe_height}"
                        src="{st.session_state.get("power_bi_iframe_url")}"
                        frameborder="0"
                        allowFullScreen="true"
                        ></iframe>
                    '''
                    ,unsafe_allow_html=True
                )

# Backoffice
if show_backoffice_tab:
    with tab_backoffice:
        st.session_state["power_bi_menu_active_tab"] = "tab_backoffice"
        col_menu, col_content = st.columns([col_menu_width, col_content_width])

        with col_menu:
            if st.button("Controle de Erros Sequenciais", key="backoffice_controle_erros_sequenciais", use_container_width=True):
                st.session_state["power_bi_menu"] = "backoffice_controle_erros_sequenciais"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiMTk0MWIyNzgtOTVkOS00MTY4LTlmZWItY2E3OTMxNWE0MWE0IiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9"
                st.session_state["power_bi_iframe_name"] = "Controle de Erros Sequenciais"
            if st.button("Controle de Recebimentos", key="backoffice_controle_recebimentos", use_container_width=True):
                st.session_state["power_bi_menu"] = "backoffice_controle_recebimentos"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiOTE4YmI2MWYtMDhhZC00OWEwLTk3OTktMTRmOTdmMzc2OTFlIiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9&pageName=9fc248609adb07e81676"
                st.session_state["power_bi_iframe_name"] = "Controle de Recebimentos"
            if st.button("Perdas Técnicas", key="backoffice_perdas_tecnicas", use_container_width=True):
                st.session_state["power_bi_menu"] = "backoffice_perdas_tecnicas"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiMGFlNDIxZjAtZjA5My00NWE4LWFhZWUtODM1ODk4ODZjMmI3IiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9&pageName=4db447d7d71e5a005320"
                st.session_state["power_bi_iframe_name"] = "Perdas Técnicas"
            if st.button("Produtividade CCI", key="backoffice_produtividade_cci", use_container_width=True):
                st.session_state["power_bi_menu"] = "backoffice_produtividade_cci"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiNmZjMDJhNzktNzg5ZS00YzIwLWFlNzgtNzI5YTVkYWIzODE4IiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9"
                st.session_state["power_bi_iframe_name"] = "Produtividade CCI"
            if st.button("Produtividade CCT", key="backoffice_produtividade_cct", use_container_width=True):
                st.session_state["power_bi_menu"] = "backoffice_produtividade_cct"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiYzFmNWViODYtNDJlZi00MmFlLWE1YWYtYjljYmU5MjRmNWM0IiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9"
                st.session_state["power_bi_iframe_name"] = "Produtividade CCT"
            if st.button("Tráfego e Faturamento", key="backoffice_trafego_faturamento", use_container_width=True):
                st.session_state["power_bi_menu"] = "backoffice_trafego_faturamento"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiODJhNmU3NjItMmQ3Ni00NWVjLTg0OGItMWMxN2JhNjRkZmYwIiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9&pageName=0ad64c088d4e2cf552fe"
                st.session_state["power_bi_iframe_name"] = "Tráfego e Faturamento"

        with col_content:
            option_backoffice = st.session_state.get("power_bi_menu", "")

            if st.session_state.get("power_bi_menu_active_tab", "") == "tab_backoffice" and option_backoffice in {
                "backoffice_controle_erros_sequenciais"
                ,"backoffice_controle_recebimentos"
                ,"backoffice_perdas_tecnicas"
                ,"backoffice_produtividade_cci"
                ,"backoffice_produtividade_cct"
                ,"backoffice_trafego_faturamento"
            }:
                st.write(st.session_state.get("power_bi_iframe_name"))
                st.markdown(
                    f'''<iframe
                        width="{power_bi_iframe_width}"
                        height="{power_bi_iframe_height}"
                        src="{st.session_state.get("power_bi_iframe_url")}"
                        frameborder="0"
                        allowFullScreen="true"
                        ></iframe>
                    '''
                    ,unsafe_allow_html=True
                )

# Comunicação
if show_communication_tab:
    with tab_communication:
        st.session_state["power_bi_menu_active_tab"] = "tab_communication"
        col_menu, col_content = st.columns([col_menu_width, col_content_width])

        with col_menu:
            if st.button("Contagem de Tráfego", key="communication_contagem_trafego", use_container_width=True):
                st.session_state["power_bi_menu"] = "communication_contagem_trafego"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiN2ZkNmU1ODYtMTI2MC00MDhjLWIzZmEtNWVkYjA4MzQ0ZGMzIiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9"
                st.session_state["power_bi_iframe_name"] = "Contagem de Tráfego"
            if st.button("Clientes e Custódia", key="communication_clientes_custodia", use_container_width=True):
                st.session_state["power_bi_menu"] = "communication_clientes_custodia"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiMTBlYmZkNWQtYzNmMC00NDBmLWFhZmMtMmUwYzBlNmMxNTM3IiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9"
                st.session_state["power_bi_iframe_name"] = "Clientes e Custódia"

        with col_content:
            option_communication = st.session_state.get("power_bi_menu", "")

            if st.session_state.get("power_bi_menu_active_tab", "") == "tab_communication" and option_communication in {
                "communication_contagem_trafego"
                ,"communication_clientes_custodia"
            }:
                # st.write(power_bi_iframe_name)
                # st.markdown(
                #     f'''<iframe
                #         width="{power_bi_iframe_width}"
                #         height="{power_bi_iframe_height}"
                #         src="{power_bi_iframe_url}"
                #         frameborder="0"
                #         allowFullScreen="true"
                #         ></iframe>
                #     '''
                #     ,unsafe_allow_html=True
                # )
                st.write(st.session_state.get("power_bi_iframe_name"))
                st.markdown(
                    f'''<iframe
                        width="{power_bi_iframe_width}"
                        height="{power_bi_iframe_height}"
                        src="{st.session_state.get("power_bi_iframe_url")}"
                        frameborder="0"
                        allowFullScreen="true"
                        ></iframe>
                    '''
                    ,unsafe_allow_html=True
                )


# Financeiro
if show_financial_tab:
    with tab_financial:
        st.session_state["power_bi_menu_active_tab"] = "tab_financial"
        col_menu, col_content = st.columns([col_menu_width, col_content_width])

        with col_menu:
            if st.button("Alteração de Faturamento", key="financial_alteracao_faturamento", use_container_width=True):
                st.session_state["power_bi_menu"] = "financial_alteracao_faturamento"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiZDcwZDUwZWYtMjg0OC00YWQ1LWIzMDUtYjI5OGNjOTRmODk2IiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9&pageName=2b9698ae14958d525414"
                st.session_state["power_bi_iframe_name"] = "Alteração de Faturamento"
            if st.button("Clientes e Custódia", key="financial_clientes_custodia", use_container_width=True):
                st.session_state["power_bi_menu"] = "financial_clientes_custodia"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiMTBlYmZkNWQtYzNmMC00NDBmLWFhZmMtMmUwYzBlNmMxNTM3IiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9"
                st.session_state["power_bi_iframe_name"] = "Clientes e Custódia"
            if st.button("Controle de Recebimentos", key="financial_controle_recebimentos", use_container_width=True):
                st.session_state["power_bi_menu"] = "financial_controle_recebimentos"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiOTE4YmI2MWYtMDhhZC00OWEwLTk3OTktMTRmOTdmMzc2OTFlIiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9&pageName=9fc248609adb07e81676"
                st.session_state["power_bi_iframe_name"] = "Controle de Recebimentos"
            if st.button("Inadimplência Atual", key="financial_inadimplencia_atual", use_container_width=True):
                st.session_state["power_bi_menu"] = "financial_inadimplencia_atual"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiYjIzN2NiMWItNjQyOC00M2U4LWExZjItZjkyNjNjN2QwNDlmIiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9&pageName=0ad64c088d4e2cf552fe"
                st.session_state["power_bi_iframe_name"] = "Inadimplência Atual"
            if st.button("Perdas Técnicas", key="financial_perdas_tecnicas", use_container_width=True):
                st.session_state["power_bi_menu"] = "financial_perdas_tecnicas"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiMGFlNDIxZjAtZjA5My00NWE4LWFhZWUtODM1ODk4ODZjMmI3IiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9&pageName=4db447d7d71e5a005320"
                st.session_state["power_bi_iframe_name"] = "Perdas Técnicas"
            if st.button("Previsto x Realizado", use_container_width=True):
                st.session_state["power_bi_menu"] = "financial_previsto_x_realizado"
                st.session_state["power_bi_iframe_url"] = ""
                st.session_state["power_bi_iframe_name"] = "Previsto x Realizado (Indisponível)"
            if st.button("Tráfego e Faturamento", key="financial_trafego_faturamento", use_container_width=True):
                st.session_state["power_bi_menu"] = "financial_trafego_faturamento"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiODJhNmU3NjItMmQ3Ni00NWVjLTg0OGItMWMxN2JhNjRkZmYwIiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9&pageName=0ad64c088d4e2cf552fe"
                st.session_state["power_bi_iframe_name"] = "Tráfego e Faturamento"

        with col_content:
            option_financial = st.session_state.get("power_bi_menu", "")

            if st.session_state.get("power_bi_menu_active_tab", "") == "tab_financial" and option_financial in {
                "financial_alteracao_faturamento"
                ,"financial_clientes_custodia"
                ,"financial_controle_recebimentos"
                ,"financial_inadimplencia_atual"
                ,"financial_perdas_tecnicas"
                ,"financial_previsto_x_realizado"
                ,"financial_trafego_faturamento"
            }:
                st.write(st.session_state.get("power_bi_iframe_name"))
                st.markdown(
                    f'''<iframe
                        width="{power_bi_iframe_width}"
                        height="{power_bi_iframe_height}"
                        src="{st.session_state.get("power_bi_iframe_url")}"
                        frameborder="0"
                        allowFullScreen="true"
                        ></iframe>
                    '''
                    ,unsafe_allow_html=True
                )

# TI Infraestrutura
if show_infrastructure_it_tab:
    with tab_infrastructure_it:
        st.session_state["power_bi_menu_active_tab"] = "tab_infrastructure_it"
        col_menu, col_content = st.columns([col_menu_width, col_content_width])

        with col_menu:
            if st.button("Controle de Infrações", key="infrastructure_it_controle_infracoes", use_container_width=True):
                st.session_state["power_bi_menu"] = "infrastructure_it_controle_infracoes"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiMmNhZmRmNTUtNDU0ZS00NDUzLTk5Y2ItMjUwOWE1YjZkMTZhIiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9"
                st.session_state["power_bi_iframe_name"] = "Controle de Infrações"
            if st.button("Controle de Recebimentos", key="infrastructure_it_controle_recebimentos", use_container_width=True):
                st.session_state["power_bi_menu"] = "infrastructure_it_controle_recebimentos"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiOTE4YmI2MWYtMDhhZC00OWEwLTk3OTktMTRmOTdmMzc2OTFlIiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9&pageName=9fc248609adb07e81676"
                st.session_state["power_bi_iframe_name"] = "Controle de Recebimentos"
            if st.button("Controle de Erros Sequenciais", key="infrastructure_it_controle_erros_sequenciais", use_container_width=True):
                st.session_state["power_bi_menu"] = "infrastructure_it_controle_erros_sequenciais"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiMTk0MWIyNzgtOTVkOS00MTY4LTlmZWItY2E3OTMxNWE0MWE0IiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9"
                st.session_state["power_bi_iframe_name"] = "Controle de Erros Sequenciais"
            if st.button("Contagem de Tráfego", key="infrastructure_it_contagem_trafego", use_container_width=True):
                st.session_state["power_bi_menu"] = "infrastructure_it_contagem_trafego"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiN2ZkNmU1ODYtMTI2MC00MDhjLWIzZmEtNWVkYjA4MzQ0ZGMzIiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9"
                st.session_state["power_bi_iframe_name"] = "Contagem de Tráfego"
            if st.button("Perdas Técnicas", key="infrastructure_it_perdas_tecnicas", use_container_width=True):
                st.session_state["power_bi_menu"] = "infrastructure_it_perdas_tecnicas"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiMGFlNDIxZjAtZjA5My00NWE4LWFhZWUtODM1ODk4ODZjMmI3IiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9&pageName=4db447d7d71e5a005320"
                st.session_state["power_bi_iframe_name"] = "Perdas Técnicas"
            if st.button("Produtividade CCT", key="infrastructure_it_produtividade_cct", use_container_width=True):
                st.session_state["power_bi_menu"] = "infrastructure_it_produtividade_cct"
                st.session_state["power_bi_iframe_url"] = "https://app.powerbi.com/view?r=eyJrIjoiYzFmNWViODYtNDJlZi00MmFlLWE1YWYtYjljYmU5MjRmNWM0IiwidCI6IjMxZjU3NDE2LTIwOWMtNDVlNy05MGQyLTkyZWUxNDQ3MDczZSJ9"
                st.session_state["power_bi_iframe_name"] = "Produtividade CCT"

        with col_content:
            option_infrastructure_it = st.session_state.get("power_bi_menu", "")

            if st.session_state.get("power_bi_menu_active_tab", "") == "tab_infrastructure_it" and option_infrastructure_it in {
                "infrastructure_it_controle_infracoes"
                ,"infrastructure_it_controle_recebimentos"
                ,"infrastructure_it_controle_erros_sequenciais"
                ,"infrastructure_it_contagem_trafego"
                ,"infrastructure_it_perdas_tecnicas"
                ,"infrastructure_it_produtividade_cct"
            }:
                st.write(st.session_state.get("power_bi_iframe_name"))
                st.markdown(
                    f'''<iframe
                        width="{power_bi_iframe_width}"
                        height="{power_bi_iframe_height}"
                        src="{st.session_state.get("power_bi_iframe_url")}"
                        frameborder="0"
                        allowFullScreen="true"
                        ></iframe>
                    '''
                    ,unsafe_allow_html=True
                )