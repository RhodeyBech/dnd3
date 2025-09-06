# Rodrigo Bechara 31/07/2025
# Página de Operações
import streamlit                as st
import pandas                   as pd
import datetime                 as dt
import json
import sqlalchemy               as sa

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
st.session_state["active_page"] = "operations"

# Carrega a barra lateral
fn.load_sidebar()

# Título
st.subheader("Operações")

# Conexões
engine_pd = fn.get_pd_connection()
engine_attri = fn.get_attri_connection()

# Inicializa flags
show_general_tab = True
show_admin_tab = False
show_backoffice_tab = False
show_financial_tab = False

# Parâmetros de largura
col_menu_width = 3
col_content_width = 20

# Define abas para mostrar
# Administração
if st.session_state.get("group_id") == 1:
    tab_admin, tab_general, tab_backoffice, tab_financial = st.tabs([
        "Administrativo"
        ,"Geral"
        ,"Backoffice"
        ,"Financeiro"
    ])
    show_admin_tab = True
    show_backoffice_tab = True
    show_financial_tab = True
# Teste de Software
elif st.session_state.get("group_id") == 2:
    tab_general, tab_backoffice, tab_financial = st.tabs([
        "Geral"
        ,"Backoffice"
        ,"Financeiro"
    ])
    show_backoffice_tab = True
    show_financial_tab = True
# Geral e Diretoria
elif st.session_state.get("group_id") in {3, 4}:
    tab_general, = st.tabs(["Geral"])
# Backoffice
elif st.session_state.get("group_id") == 5:
    tab_general, tab_backoffice = st.tabs(["Geral", "Backoffice"])
    show_backoffice_tab = True
# Financeiro
elif st.session_state.get("group_id") == 6:
    tab_general, tab_financial = st.tabs(["Geral", "Financeiro"])
    show_financial_tab = True


# ||========================================================================================================================================||
# ||========================================================================================================================================||
# ||    BACKOFFICE                                                                                                                          ||
# ||========================================================================================================================================||
# ||========================================================================================================================================||
if show_backoffice_tab:
    with tab_backoffice:

        col_menu, col_content = st.columns([col_menu_width, col_content_width])
        with col_menu:
            st.markdown("##### Nevada")
            if st.button("Descarte de Passagens Pagas", key="backoffice_nevada_discards_paid_passages", use_container_width=True):
                st.session_state["operations_backoffice"] = "backoffice_nevada_discards_paid_passages"
                if "operations_backoffice_nevada" in st.session_state:
                    del st.session_state["operations_backoffice_nevada"]

        with col_content:
            option_backoffice = st.session_state.get("operations_backoffice")

            # ||=== NEVADA =================================================================================================================||
            if option_backoffice == "backoffice_nevada_discards_paid_passages":
                tab_01, tab_02 = st.tabs(["Descarte de Passagens", "Histórico"])
                with tab_01:
                    st.write("Nevada -- Descarte de Passagens Pagas")
                    # df_backoffice_nevada_discards_paid_passages = pd.DataFrame()

                    col1, col2, col3, col4, col5 = st.columns([3, 4, 8, 2, 3])
                    with col1:
                        fn.shift_top(18)
                        if st.button("Descartar Passagens", key="backoffice_nevada_discards_paid_passages_nevada", use_container_width=True):
                            st.session_state["operations_backoffice_nevada_discards_paid_passages"] = "backoffice_nevada_discards_paid_passages_discard"
                    with col2:
                        backoffice_nevada_discards_paid_passages_initial_date = st.date_input("Data Inicial:", value=dt.date.today() - dt.timedelta(days=36), format="DD/MM/YYYY", key="backoffice_nevada_discards_paid_passages_initial_date")
                        backoffice_nevada_discards_paid_passages_end_date = st.date_input("Data Final:", value=dt.date.today() - dt.timedelta(days=33), format="DD/MM/YYYY", key="backoffice_nevada_discards_paid_passages_end_date")
                    with col3:
                        backoffice_nevada_discards_paid_passages_user = st.text_input("Usuário:", key="backoffice_nevada_discards_paid_passages_user")
                        backoffice_nevada_discards_paid_passages_access_key = st.text_input("Chave de Acesso:", key="backoffice_nevada_discards_paid_passages_access_key")
                    # with col4:
                        # placeholder_backoffice_nevada_discards_paid_passages_result = st.empty()

                    placeholder_backoffice_nevada_discards_paid_passages = st.empty()

                    option_backoffice_nevada_discards_paid_passages = st.session_state.get("operations_backoffice_nevada_discards_paid_passages")
                    if option_backoffice_nevada_discards_paid_passages == "backoffice_nevada_discards_paid_passages_discard":
                        if not backoffice_nevada_discards_paid_passages_user or not backoffice_nevada_discards_paid_passages_access_key:
                            placeholder_backoffice_nevada_discards_paid_passages.error("Processo Cancelado. Usuário e/ou Chave de Acesso inválido(s).")
                            if "operations_backoffice_nevada_discards_paid_passages" in st.session_state:
                                del st.session_state["operations_backoffice_nevada_discards_paid_passages"]
                            if "backoffice_nevada_discards_paid_passages_result_str" in st.session_state:
                                del st.session_state["backoffice_nevada_discards_paid_passages_result_str"]
                        else:
                            with st.form("backoffice_nevada_discards_paid_passages_confirm", width=700):
                                # Confirmação
                                st.markdown(f"##### Deseja descartar as passagens paga do dia {backoffice_nevada_discards_paid_passages_initial_date.strftime("%d/%m/%Y")} ao dia {backoffice_nevada_discards_paid_passages_end_date.strftime("%d/%m/%Y")}?")

                                # Cria colunas
                                col1, col2, cal3 = st.columns([1, 1, 4])
                                with col1:
                                    bt_yes_backoffice_nevada_discards_paid_passages = st.form_submit_button("Sim", use_container_width=True)
                                with col2:
                                    bt_no_backoffice_nevada_discards_paid_passages = st.form_submit_button("Não", use_container_width=True)

                                # Caso Não
                                if bt_no_backoffice_nevada_discards_paid_passages:
                                    if "operations_backoffice_nevada_discards_paid_passages" in st.session_state:
                                        del st.session_state["operations_backoffice_nevada_discards_paid_passages"]
                                    st.rerun()
                                elif bt_yes_backoffice_nevada_discards_paid_passages:
                                    placeholder_backoffice_nevada_discards_paid_passages.warning("Executando...")
                                    st.session_state["backoffice_nevada_discards_paid_passages_result_str"] = fn.discards_paid_passages(backoffice_nevada_discards_paid_passages_initial_date, backoffice_nevada_discards_paid_passages_end_date, backoffice_nevada_discards_paid_passages_user, backoffice_nevada_discards_paid_passages_access_key)
                                    st.session_state["backoffice_nevada_discards_paid_passages_result_datetime"] = f"Execução: {dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
                                    del st.session_state["operations_backoffice_nevada_discards_paid_passages"]
                                    st.rerun()

                    if "backoffice_nevada_discards_paid_passages_result_str" in st.session_state:
                        str_discards_paid_passages_response = st.session_state.get("backoffice_nevada_discards_paid_passages_result_str")
                        st.write(st.session_state.get("backoffice_nevada_discards_paid_passages_result_datetime"))
                        if "DELETE" in str_discards_paid_passages_response:
                            placeholder_backoffice_nevada_discards_paid_passages_result = st.write(str_discards_paid_passages_response)
                        else:
                            # Separa JSON
                            discards_paid_passages_response = json.loads(str_discards_paid_passages_response)
                            # Obtém DataFrame
                            backoffice_nevada_discards_paid_passages_result_df = pd.DataFrame(discards_paid_passages_response["failedItems"])
                            # Qtde Já Descartada
                            if not backoffice_nevada_discards_paid_passages_result_df.empty:
                                discards_paid_passages_response_already_discarded = backoffice_nevada_discards_paid_passages_result_df[backoffice_nevada_discards_paid_passages_result_df["error"] == "Capture already discarded"].shape[0]
                                discards_paid_passages_response_already_discarded = f"{discards_paid_passages_response_already_discarded:,}".replace(",", ".")
                            else:
                                discards_paid_passages_response_already_discarded = "0"
                            # Qtde de Sucessos
                            discards_paid_passages_response_succeeded = f"{discards_paid_passages_response["succeeded"]:,}".replace(",", ".")
                            # Remove já descartados e não encontrados
                            backoffice_nevada_discards_paid_passages_result_df = backoffice_nevada_discards_paid_passages_result_df[~backoffice_nevada_discards_paid_passages_result_df["error"].isin(["Register not found", "Capture already discarded"])]
                            # Qtde de Falhas
                            if not backoffice_nevada_discards_paid_passages_result_df.empty:
                                discards_paid_passages_response_failed = backoffice_nevada_discards_paid_passages_result_df.shape[0]
                                discards_paid_passages_response_failed = f"{discards_paid_passages_response_failed:,}".replace(",", ".")
                            else:
                                discards_paid_passages_response_failed = "0"
                            placeholder_backoffice_nevada_discards_paid_passages_result = st.write(f"""
                                Retorno da Execução                                                                 {chr(13)}
                                Qtde Descartada: {discards_paid_passages_response_succeeded}                        {chr(13)}
                                Qtde Descartada Anteriormente: {discards_paid_passages_response_already_discarded}  {chr(13)}
                                Qtde de Falhas: {discards_paid_passages_response_failed}                            {chr(13)}
                            """)
                            if not backoffice_nevada_discards_paid_passages_result_df.empty:
                                st.dataframe(backoffice_nevada_discards_paid_passages_result_df, height=600, hide_index=True)
                            # Grava Log
                            create_log_discards_paid_passages_return = fn.create_log_discards_paid_passages(
                                initial_date=backoffice_nevada_discards_paid_passages_initial_date
                                ,end_date=backoffice_nevada_discards_paid_passages_end_date
                                ,access_user=backoffice_nevada_discards_paid_passages_user
                                ,count_discarded=int(discards_paid_passages_response_succeeded.replace(".", ""))
                                ,count_already_discarded=int(discards_paid_passages_response_already_discarded.replace(".", ""))
                                ,count_failed=int(discards_paid_passages_response_failed.replace(".", ""))
                            )
                            if create_log_discards_paid_passages_return != None:
                                st.error(create_log_discards_paid_passages_return)

                        del st.session_state["backoffice_nevada_discards_paid_passages_result_str"]

                with tab_02:
                    placeholder_backoffice_nevada_discards_paid_passages = st.empty()
                    st.write("Nevada -- Histórico de Descarte de Passagens Pagas")
                    # df_backoffice_nevada_discards_paid_passages = pd.DataFrame()

                    col1, col2, col3, col4, col5 = st.columns([3, 4, 8, 2, 3])
                    placeholder_backoffice_nevada_discards_paid_passages_search = st.empty()
                    with col1:
                        fn.shift_top(18)
                        if st.button("Pesquisar", key="backoffice_nevada_discards_paid_passages_nevada_search", use_container_width=True):
                            st.session_state["operations_backoffice_nevada_discards_paid_passages"] = "backoffice_nevada_discards_paid_passages_discard_search"
                    with col2:
                        backoffice_nevada_discards_paid_passages_search_initial_date = st.date_input("Data Inicial:", value=fn.dateadd(fn.day, -6, dt.datetime.now()), format="DD/MM/YYYY", key="backoffice_nevada_discards_paid_passages_search_initial_date")
                        backoffice_nevada_discards_paid_passages_search_end_date = st.date_input("Data Final:", value=dt.date.today(), format="DD/MM/YYYY", key="backoffice_nevada_discards_paid_passages_search_end_date")

                    option_backoffice_nevada_discards_paid_passages = st.session_state.get("operations_backoffice_nevada_discards_paid_passages")
                    if option_backoffice_nevada_discards_paid_passages == "backoffice_nevada_discards_paid_passages_discard_search":
                        placeholder_backoffice_nevada_discards_paid_passages_search.warning("Pesquisando...")
                        # Escreve query
                        query_backoffice_nevada_discards_paid_passages_discard_search = f"""
                            SELECT
                                ExecutionId                                     AS [Nº]
                                ,FORMAT(ExecutedAt, 'dd/MM/yyyy HH:mm:ss')      AS [Executado em]
                                ,ExecutedBy                                     AS [Executado por]
                                ,FORMAT(InitialDate, 'dd/MM/yyyy')              AS [Data Inicial]
                                ,FORMAT(EndDate, 'dd/MM/yyyy')                  AS [Data Final]
                                ,AccessUser                                     AS [Usuário de Acesso]
                                ,REPLACE(
                                    FORMAT(Count_Discarded, '#,##0')
                                    ,',', '.')                                  AS [Qtde Descartada]
                                ,REPLACE(
                                    FORMAT(Count_AlreadyDiscarded, '#,##0')
                                    ,',', '.')                                  AS [Qtde Descartada Anteriormente]
                                ,REPLACE(
                                    FORMAT(Count_Failed, '#,##0')
                                    ,',', '.')                                  AS [Qtde de Falhas]
                            FROM Nexus.log.Operation_DiscardPaidPassages
                            WHERE
                                CAST(ExecutedAt AS DATE) BETWEEN '{backoffice_nevada_discards_paid_passages_search_initial_date.strftime("%Y-%m-%d")}' AND '{backoffice_nevada_discards_paid_passages_search_end_date.strftime("%Y-%m-%d")}'
                            ORDER BY
                                ExecutedAt DESC
                        """

                        # Consulta ao banco
                        df_backoffice_nevada_discards_paid_passages = pd.read_sql(query_backoffice_nevada_discards_paid_passages_discard_search, engine_pd)
                        st.session_state["operation_backoffice_nevada_discards_paid_passages_datetime"] = f"{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
                        st.session_state["backoffice_nevada_discards_paid_passages_df"] = df_backoffice_nevada_discards_paid_passages
                        placeholder_backoffice_nevada_discards_paid_passages_search.empty()

                        del st.session_state["operations_backoffice_nevada_discards_paid_passages"]
                        st.rerun()

                    if "backoffice_nevada_discards_paid_passages_df" in st.session_state:
                        if not st.session_state.get("backoffice_nevada_discards_paid_passages_df").empty:
                            # Exibe em tela
                            rows_number = "{:,}".format(st.session_state.get("backoffice_nevada_discards_paid_passages_df").shape[0]).replace(",", ".")
                            st.text(f"{st.session_state["operation_backoffice_nevada_discards_paid_passages_datetime"]}\t\tRegistros: {rows_number}")
                            st.dataframe(st.session_state.get("backoffice_nevada_discards_paid_passages_df"), height=600, hide_index=True)
                        else:
                            placeholder_backoffice_nevada_discards_paid_passages_search.error("Nenhum registro encontrado.")
                            if "backoffice_nevada_discards_paid_passages_df" in st.session_state:
                                del st.session_state["backoffice_nevada_discards_paid_passages_df"]


# ||========================================================================================================================================||
# ||========================================================================================================================================||
# ||    FINANCEIRO                                                                                                                          ||
# ||========================================================================================================================================||
# ||========================================================================================================================================||
if show_financial_tab:
    with tab_financial:

        col_menu, col_content = st.columns([col_menu_width, col_content_width])
        with col_menu:
            st.markdown("##### kapsch")
            if st.button("Recebimentos OSA InteropFlex", key="financial_kapsch_ifx_payment_transfer", use_container_width=True):
                st.session_state["operations_financial"] = "financial_kapsch_ifx_payment_transfer"
                if "operations_financial_kapsch" in st.session_state:
                    del st.session_state["operations_financial_kapsch"]

        with col_content:
            option_financial = st.session_state.get("operations_financial")

            # ||=== kapsch ==================================================================================================================||
            if option_financial == "financial_kapsch_ifx_payment_transfer":
                tab_financial_kapsch_search_report, tab_financial_kapsch_report_import = st.tabs(["Pesquisar Relatório", "Importar Relatório"])

                with tab_financial_kapsch_search_report:
                    df_financial_kapsch_ifx_payment_transfer_search = pd.DataFrame()
                    col1, col2, col3, col4 = st.columns([3, 3, 4, 10])
                    with col1:
                        fn.shift_top(18)
                        if st.button("Pesquisar", key="financial_kapsch_ifx_payment_transfer_search",  use_container_width=True):
                            st.session_state["operations_financial_kapsch_ifx_payment_transfer"] = "financial_kapsch_ifx_payment_transfer_search"
                        csv_financial_kapsch_ifx_payment_transfer_search = df_financial_kapsch_ifx_payment_transfer_search.to_csv(index=False, sep=";")
                        if "financial_kapsch_ifx_payment_transfer_df" in st.session_state:
                            if not st.session_state.get("financial_kapsch_ifx_payment_transfer_df").empty:
                                df_financial_kapsch_ifx_payment_transfer_search = st.session_state.get("financial_kapsch_ifx_payment_transfer_df")
                                csv_financial_kapsch_ifx_payment_transfer_search = df_financial_kapsch_ifx_payment_transfer_search.to_csv(index=False, sep=";")
                        st.download_button(
                            label="Baixar CSV"
                            ,key="csv_financial_kapsch_ifx_payment_transfer_search"
                            ,data=csv_financial_kapsch_ifx_payment_transfer_search.encode("utf-8-sig")
                            ,file_name="Recebimentos OSA InteropFlex.csv"
                            ,mime="text/csv"
                            ,use_container_width=True
                        )
                    with col2:
                        financial_kapsch_ifx_payment_transfer_initial_date = st.date_input("Data Inicial:", value=fn.beginning_of_month(dt.date.today()), format="DD/MM/YYYY", key="financial_kapsch_ifx_payment_transfer_initial_date")
                        financial_kapsch_ifx_payment_transfer_ending_date = st.date_input("Data Inicial:", value=fn.end_of_month(dt.date.today()), format="DD/MM/YYYY", key="financial_kapsch_ifx_payment_transfer_ending_date")

                    placeholder_financial_kapsch_ifx_payment_transfer_search = st.empty()

                    option_backoffice_general = st.session_state.get("operations_financial_kapsch_ifx_payment_transfer")
                    if option_backoffice_general == "financial_kapsch_ifx_payment_transfer_search":
                        placeholder_financial_kapsch_ifx_payment_transfer_search.warning("Pesquisando...")

                        # Verifica validade das datas
                        financial_kapsch_ifx_payment_transfer_date_diff = financial_kapsch_ifx_payment_transfer_ending_date - financial_kapsch_ifx_payment_transfer_initial_date
                        if financial_kapsch_ifx_payment_transfer_date_diff.days < 0:
                            placeholder_financial_kapsch_ifx_payment_transfer_search.error("Processo Cancelado. Período de datas não confere.")
                            if "operations_financial_kapsch_ifx_payment_transfer" in st.session_state:
                                del st.session_state["operations_financial_kapsch_ifx_payment_transfer"]
                            if "financial_kapsch_ifx_payment_transfer_df" in st.session_state:
                                del st.session_state["financial_kapsch_ifx_payment_transfer_df"]
                            st.stop()

                        # Escreve query
                        query_inancial_kapsch_ifx_payment_transfer = f"""
                           SELECT
                                OSA
                                ,FORMAT(TransferDate, 'dd/MM/yyyy')             AS [Data da Transferência]
                                ,'R$ ' + FORMAT(TransferValue, '#,##0.00')      AS [Valor da Transferência]
                                ,FORMAT(PassageDate, 'dd/MM/yyyy')              AS [Data da Passagem]
                                ,'R$ ' + FORMAT(PassageValue, '#,##0.00')       AS [Valor da Passagem]
                                ,'R$ ' + FORMAT(ValueDifference, '#,##0.00')    AS [Diferença no Valor]
                            FROM Nexus.ifx.PaymentTransfer
                            WHERE
                                CAST(TransferDate AS DATE) BETWEEN '{financial_kapsch_ifx_payment_transfer_initial_date.strftime('%Y-%m-%d')}' AND '{financial_kapsch_ifx_payment_transfer_ending_date.strftime('%Y-%m-%d')}'
                        """

                        # Consulta ao banco
                        df_financial_kapsch_ifx_payment_transfer_search = pd.read_sql(query_inancial_kapsch_ifx_payment_transfer, engine_pd)

                        st.session_state["financial_kapsch_ifx_payment_transfer_datetime"] = f"{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"

                        # Constroi dataframe
                        if not df_financial_kapsch_ifx_payment_transfer_search.empty:
                            # Exibe em tela
                            st.session_state["financial_kapsch_ifx_payment_transfer_df"] = df_financial_kapsch_ifx_payment_transfer_search
                            csv_financial_kapsch_ifx_payment_transfer_search = df_financial_kapsch_ifx_payment_transfer_search.to_csv(index=False, sep=";")
                            placeholder_financial_kapsch_ifx_payment_transfer_search.empty()
                        else:
                            placeholder_financial_kapsch_ifx_payment_transfer_search.error("Nenhum registro encontrado.")

                        del st.session_state["operations_financial_kapsch_ifx_payment_transfer"]
                        st.rerun()

                    if "financial_kapsch_ifx_payment_transfer_df" in st.session_state:
                        if not st.session_state.get("financial_kapsch_ifx_payment_transfer_df").empty:
                            # Exibe em tela
                            rows_number = "{:,}".format(st.session_state.get("financial_kapsch_ifx_payment_transfer_df").shape[0]).replace(",", ".")
                            st.text(f"{st.session_state["financial_kapsch_ifx_payment_transfer_datetime"]}\t\tQtde de Registros: {rows_number}")
                            st.dataframe(st.session_state.get("financial_kapsch_ifx_payment_transfer_df"), height=600, hide_index=True)


                with tab_financial_kapsch_report_import:
                    col1, col2, col3 = st.columns([3, 4, 13])
                    with col1:
                        fn.shift_top(26)
                        if st.button("Importar Relatório", key="financial_kapsch_ifx_payment_transfer_import", use_container_width=True):
                            st.session_state["operations_financial_kapsch"] = "financial_kapsch_ifx_payment_transfer_import"

                    with col2:
                        st.write("Selecine um aquivo:")
                        financial_kapsch_ifx_payment_transfer_files = ""
                        financial_kapsch_ifx_payment_transfer_files = st.file_uploader("Arquivo - Recebimentos OSA InteropFlex", type=["csv"], accept_multiple_files=True, label_visibility="collapsed")

                    placeholder_financial_kapsch_ifx_payment_transfer_import = st.empty()

                    option_financial_kapsch_ifx_payment_transfer_import = st.session_state.get("operations_financial_kapsch")
                    if option_financial_kapsch_ifx_payment_transfer_import == "financial_kapsch_ifx_payment_transfer_import":
                        placeholder_financial_kapsch_ifx_payment_transfer_import.warning("Importando...")

                        if not financial_kapsch_ifx_payment_transfer_files:
                            if "operations_financial_kapsch" in st.session_state:
                                del st.session_state["operations_financial_kapsch"]
                            placeholder_financial_kapsch_ifx_payment_transfer_import.error("Processo Cancelado. Nenhum arquivo selecionado.")
                            st.stop()
                        else:
                            # Carrega arquivos
                            dfs = []
                            for file in financial_kapsch_ifx_payment_transfer_files:
                                df_temp = pd.read_csv(file)
                                dfs.append(df_temp)

                            # Junta DataFrame
                            df_financial_kapsch_ifx_payment_transfer_file = pd.concat(dfs, ignore_index=True)

                            # FORMATA ATBELA
                            # Remove linhas de somatórios
                            df_financial_kapsch_ifx_payment_transfer_file = df_financial_kapsch_ifx_payment_transfer_file.dropna(subset=["Data da passagens"])
                            # Formata colunas
                            for col in df_financial_kapsch_ifx_payment_transfer_file.columns:
                                # Formata valores
                                if "Valor " in col or "Diferenças " in col:
                                    df_financial_kapsch_ifx_payment_transfer_file[col] = (
                                        df_financial_kapsch_ifx_payment_transfer_file[col]
                                        .astype(str)
                                        .str.replace(r"R\$\s*", "", regex=True)
                                        .str.strip()
                                        .str.replace(".", "", regex=False)
                                        .str.replace(",", ".", regex=False)
                                        .apply(pd.to_numeric, errors="coerce")
                                    )
                                # Formata datas
                                elif "Data " in col:
                                    df_financial_kapsch_ifx_payment_transfer_file[col] = pd.to_datetime(
                                        df_financial_kapsch_ifx_payment_transfer_file[col].astype(str).str.strip()
                                        ,dayfirst=True
                                        ,errors="coerce"
                                    )
                                # Formata datas
                                elif col == "Alvo":
                                    df_financial_kapsch_ifx_payment_transfer_file[col] = (
                                        df_financial_kapsch_ifx_payment_transfer_file[col]
                                        .astype(str)
                                        .str.replace("Greenpass", "GreenPass")
                                        .str.replace("Conectcar", "ConectCar")
                                        .str.replace("MoveMais", "Move Mais")
                                        .str.strip()
                                    )

                            with engine_pd.begin() as conn:
                                count_insert = 0
                                max_index = df_financial_kapsch_ifx_payment_transfer_file.shape[0] - 1
                                for i, (index, row) in enumerate(df_financial_kapsch_ifx_payment_transfer_file.iterrows()):
                                    count_insert += 1
                                    # Formata datas
                                    data_pagamento = pd.to_datetime(row["Data de pagamento"], dayfirst=True).strftime("%Y-%m-%d")
                                    data_passagens = pd.to_datetime(row["Data da passagens"], dayfirst=True).strftime("%Y-%m-%d")

                                    # Monta trecho de VALUES
                                    values_str = f"""('{row["Alvo"]}', '{data_pagamento}', {row["Valor a ser pago"]}, '{data_passagens}', {row["Valor da passagens"]}, {row["Diferenças de pagamento"]})"""

                                    # Junta com vírgula se não for a primeira linha
                                    if count_insert == 1:
                                        query_insert_payment_transfer_values = values_str
                                    else:
                                        query_insert_payment_transfer_values += f",\n{values_str}"

                                    if count_insert == 1000 or i == max_index:
                                        query_insert_payment_transfer = sa.text(f"""
                                            DECLARE @PaymentTransfer        TABLE (
                                                OSA                     VARCHAR (20)
                                                ,TransferDate           DATE
                                                ,TransferValue          DECIMAL (10, 2)
                                                ,PassageDate            DATE
                                                ,PassageValue           DECIMAL (10, 2)
                                                ,ValueDifference        DECIMAL (10, 2)
                                            )
                                            INSERT INTO @PaymentTransfer (
                                                OSA
                                                ,TransferDate
                                                ,TransferValue
                                                ,PassageDate
                                                ,PassageValue
                                                ,ValueDifference
                                            )
                                            VALUES
                                                {query_insert_payment_transfer_values}
                                            -- INSERT
                                            INSERT INTO Nexus.ifx.PaymentTransfer (
                                                OSA
                                                ,TransferDate
                                                ,TransferValue
                                                ,PassageDate
                                                ,PassageValue
                                                ,ValueDifference
                                            )
                                                SELECT
                                                    TEMP.OSA
                                                    ,TEMP.TransferDate
                                                    ,TEMP.TransferValue
                                                    ,TEMP.PassageDate
                                                    ,TEMP.PassageValue
                                                    ,TEMP.ValueDifference
                                                FROM @PaymentTransfer               AS TEMP
                                                LEFT JOIN Nexus.ifx.PaymentTransfer AS PT
                                                    ON PT.OSA = TEMP.OSA
                                                    AND PT.TransferDate = TEMP.TransferDate
                                                    AND PT.PassageDate = TEMP.PassageDate
                                                WHERE
                                                    PT.TransferDate IS NULL
                                            -- UPDATE
                                            UPDATE PT
                                                SET
                                                    PT.TransferValue        = TEMP.TransferValue
                                                    ,PT.PassageValue        = TEMP.PassageValue
                                                    ,PT.ValueDifference     = TEMP.ValueDifference
                                                FROM Nexus.ifx.PaymentTransfer  AS PT
                                                LEFT JOIN @PaymentTransfer      AS TEMP
                                                    ON TEMP.OSA = PT.OSA
                                                    AND TEMP.TransferDate = PT.TransferDate
                                                    AND TEMP.PassageDate = PT.PassageDate
                                                WHERE
                                                    PT.TransferDate IS NOT NULL
                                        """)
                                        conn.execute(query_insert_payment_transfer)
                                        count_insert = 0
                                        query_insert_payment_transfer_values = ""


                            # Fim
                            placeholder_financial_kapsch_ifx_payment_transfer_import.success("Processo Concluído.")
                            if "operations_financial_kapsch" in st.session_state:
                                del st.session_state["operations_financial_kapsch"]