# Rodrigo Bechara 18/08/2025
# Página de controle do RPA
import streamlit                as st
import pandas                   as pd
import datetime                 as dt
import time
import sqlalchemy               as sa
# import plotly.express           as px
# import plotly.graph_objects     as go

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
    # st.switch_page("pages/login")

if st.session_state.get("access_level_id", 3) != 1:
    st.switch_page("pages/home.py")
    # st.switch_page("pages/login")

# Configuração da página
st.set_page_config(
    page_title="Nexus"
    ,page_icon="https://www.csg.com.br/build/assets/favicon-c752c7b3.png"
    ,layout="wide"
)

# Ajusta cabeçalho da página
fn.hidden_header()

# Define página ativa
st.session_state["active_page"] = "rpa"

# Carrega a barra lateral
fn.load_sidebar()

# Título
st.subheader("RPA")

# Conexões
engine_pd = fn.get_pd_connection()

# Parâmetros de largura
col_menu_width = 3
col_content_width = 20

# Definições
dict_boolean_list = {
    "Não": 0
    ,"Sim": 1
}
dict_schedule_frequency_list = {
    "Uma vez apenas": 1
    ,"Diariamente": 2
    ,"Semanalmente": 3
    ,"Mensalmente": 4
}
dict_schedule_recurrence_list = {
    "No horário especificado": 1
    ,"Minuto(s)": 2
    ,"Hora(s)": 3
}
dict_hour_list = {
    "00:00:00": 1
    ,"00:15:00": 2
    ,"00:30:00": 3
    ,"00:45:00": 4
    ,"01:00:00": 5
    ,"01:15:00": 6
    ,"01:30:00": 7
    ,"01:45:00": 8
    ,"02:00:00": 9
    ,"02:15:00": 10
    ,"02:30:00": 11
    ,"02:45:00": 12
    ,"03:00:00": 13
    ,"03:15:00": 14
    ,"03:30:00": 15
    ,"03:45:00": 16
    ,"04:00:00": 17
    ,"04:15:00": 18
    ,"04:30:00": 19
    ,"04:45:00": 20
    ,"05:00:00": 21
    ,"05:15:00": 22
    ,"05:30:00": 23
    ,"05:45:00": 24
    ,"06:00:00": 25
    ,"06:15:00": 26
    ,"06:30:00": 27
    ,"06:45:00": 28
    ,"07:00:00": 29
    ,"07:15:00": 30
    ,"07:30:00": 31
    ,"07:45:00": 32
    ,"08:00:00": 33
    ,"08:15:00": 34
    ,"08:30:00": 35
    ,"08:45:00": 36
    ,"09:00:00": 37
    ,"09:15:00": 38
    ,"09:30:00": 39
    ,"09:45:00": 40
    ,"10:00:00": 41
    ,"10:15:00": 42
    ,"10:30:00": 43
    ,"10:45:00": 44
    ,"11:00:00": 45
    ,"11:15:00": 46
    ,"11:30:00": 47
    ,"11:45:00": 48
    ,"12:00:00": 49
    ,"12:15:00": 50
    ,"12:30:00": 51
    ,"12:45:00": 52
    ,"13:00:00": 53
    ,"13:15:00": 54
    ,"13:30:00": 55
    ,"13:45:00": 56
    ,"14:00:00": 57
    ,"14:15:00": 58
    ,"14:30:00": 59
    ,"14:45:00": 60
    ,"15:00:00": 61
    ,"15:15:00": 62
    ,"15:30:00": 63
    ,"15:45:00": 64
    ,"16:00:00": 65
    ,"16:15:00": 66
    ,"16:30:00": 67
    ,"16:45:00": 68
    ,"17:00:00": 69
    ,"17:15:00": 70
    ,"17:30:00": 71
    ,"17:45:00": 72
    ,"18:00:00": 73
    ,"18:15:00": 74
    ,"18:30:00": 75
    ,"18:45:00": 76
    ,"19:00:00": 77
    ,"19:15:00": 78
    ,"19:30:00": 79
    ,"19:45:00": 80
    ,"20:00:00": 81
    ,"20:15:00": 82
    ,"20:30:00": 83
    ,"20:45:00": 84
    ,"21:00:00": 85
    ,"21:15:00": 86
    ,"21:30:00": 87
    ,"21:45:00": 88
    ,"22:00:00": 89
    ,"22:15:00": 90
    ,"22:30:00": 91
    ,"22:45:00": 92
    ,"23:00:00": 93
    ,"23:15:00": 94
    ,"23:30:00": 95
    ,"23:45:00": 96
    ,"23:59:59": 97
}


# Abas
tab_execution, tab_scheduling = st.tabs([
    "Execução"
    ,"Agendamento"
])

with tab_execution:
    # Atualiza status dos bots
    fn.update_status_runner01()
    col_menu, col_content = st.columns([col_menu_width, col_content_width])

    with col_menu:
        st.subheader("Monitor")
        # if st.button("Update Status Runner01", key="update_status_runner01", use_container_width=True):
        #     fn.update_status_runner01()
        st.text(f"Runner 01:\t\t{"🟢 On" if fn.get_runner01_status() else "🔴 Off"}")

    with col_content:
        st.subheader("Histórico de Execuções")
        col1, col2 = st.columns([1, 9])
        with col1:
            if st.button("Pesquisar", key="rpa_execution_get_log", use_container_width=True):
                st.session_state["rpa_execution"] = "rpa_execution_get_log"

        placeholder_rpa_execution = st.empty()

        option_rpa = st.session_state.get("rpa_execution")
        if option_rpa == "rpa_execution_get_log":
            query_rpa_execution_get_log = f"""
                SELECT
                    R.RoutineName                                   AS Rotina
                    ,FORMAT(EL.Beginning, 'dd/MM/yyyy HH:mm:ss')    AS [Início]
                    ,FORMAT(EL.[End], 'dd/MM/yyyy HH:mm:ss')        AS [Final]
                    ,EL.[Status]
                    ,EL.[Message]                                   AS Mensagem
                FROM Nexus.rpa.ExecutionLog     AS EL
                LEFT JOIN Nexus.rpa.[Routine]   AS R
                    ON R.Id = EL.RoutineId
                ORDER BY
                    EL.Beginning DESC
            """
            # Consulta ao banco
            df_rpa_execution_get_log = pd.read_sql(query_rpa_execution_get_log, engine_pd)
            st.session_state["rpa_execution_get_log_datetime"] = f"{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            st.session_state["rpa_execution_get_log_df"] = df_rpa_execution_get_log

            del st.session_state["rpa_execution"]
            st.rerun()

        if "rpa_execution_get_log_df" in st.session_state:
            if not st.session_state.get("rpa_execution_get_log_df").empty:
                # Exibe em tela
                rows_number = "{:,}".format(st.session_state.get("rpa_execution_get_log_df").shape[0]).replace(",", ".")
                st.text(f"{st.session_state["rpa_execution_get_log_datetime"]}\t\tRegistros: {rows_number}")
                st.dataframe(st.session_state.get("rpa_execution_get_log_df"), height=600, hide_index=True)
                # st.dataframe(
                #     st.session_state.get("rpa_execution_get_log_df").style
                #         .set_properties(subset=["Rotina"], **{'min-width': '100px'})
                #         .set_properties(subset=["Início"], **{'min-width': '100px'})
                #         .set_properties(subset=["Final"], **{'min-width': '100px'})
                #         .set_properties(subset=["Status"], **{'min-width': '100px'})
                #     ,hide_index=True
                # )
            else:
                placeholder_rpa_execution.error("Nenhum registro encontrado.")
                if "rpa_execution_get_log_df" in st.session_state:
                    del st.session_state["rpa_execution_get_log_df"]


with tab_scheduling:
    col_menu, col_content = st.columns([col_menu_width, col_content_width])

    with col_menu:
        if st.button("Novo Agendamento", key="rpa_new_scheduling", use_container_width=True):
            st.session_state["rpa_scheduling"] = "rpa_new_scheduling"
            # if "operations_backoffice_nevada" in st.session_state:
            #     del st.session_state["operations_backoffice_nevada"]

    rpa_option = st.session_state.get("rpa_scheduling", "")


    # Lista de sgendamentos
    st.subheader("Agendamentos")
    placeholder_rpa_edit_routine = st.warning("Pesquisando...")
    # print(f"{dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}")
    with engine_pd.connect() as conn:
        
        # if not "rpa_edit_routine_id" in st.session_state:
        routines = conn.execute(sa.text(f"""
            SELECT
                R.Id
                ,R.RoutineName
                ,R.RoutineDescription
                ,R.Enabled
                ,FORMAT(S.Beginning, 'dd/MM/yyyy')      AS Beginning
                ,FORMAT(S.[End], 'dd/MM/yyyy')          AS [End]
                ,SF.FrequencyDescription
                ,S.RecurrenceTime
                ,SR.RecurrenceDescription
                ,S.StartTime
                ,S.EndTime
            FROM Nexus.rpa.[Routine]                    AS R
            LEFT JOIN Nexus.rpa.[Schedule]              AS S
                ON S.RoutineId = R.Id
            LEFT JOIN Nexus.rpa.[ScheduleFrequency]     AS SF
                ON SF.Id = S.FrequencyId
            LEFT JOIN Nexus.rpa.[ScheduleRecurrence]    AS SR
                ON SR.Id = S.RecurrenceId
        """)).fetchall()

        placeholder_rpa_edit_routine.empty()

        # Largura das colunas do agendamento
        scheduling_columns_width = [
            6
            ,3
            ,8
            ,16
            ,6
            ,7
            ,7
            ,8
            ,8
            ,8
            ,7
            ,7
        ]
        # Cabeçalho
        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12 = st.columns(scheduling_columns_width)
        col2.markdown("**ID**")
        col3.markdown("**ROTINA**")
        col4.markdown("**DESCRIÇÃO**")
        col5.markdown("**ATIVO**")
        col6.markdown("**INÍCIO**")
        col7.markdown("**FIM**")
        col8.markdown("**FREQUÊNCIA**")
        col9.markdown("**TEMPO DA RECORRÊNCIA**")
        col10.markdown("**RECORRÊNCIA**")
        col11.markdown("**HORA DE INÍCIO**")
        col12.markdown("**HORA DE TÉRMINO**")

        # Cria tabela de dados
        for routine in routines:
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12 = st.columns(scheduling_columns_width)
            if col1.button("Editar", key=f"edit_{routine.Id}", use_container_width=True):
                st.session_state["rpa_edit_routine_id"] = routine.Id
            col2.markdown(routine.Id)
            col3.markdown(routine.RoutineName)
            col4.markdown(routine.RoutineDescription)
            col5.markdown("✅ Sim" if routine.Enabled == 1 else "❌ Não")
            col6.markdown(routine.Beginning)
            col7.markdown(routine.End)
            col8.markdown(routine.FrequencyDescription)
            col9.markdown(routine.RecurrenceTime)
            col10.markdown(routine.RecurrenceDescription)
            col11.markdown(routine.StartTime)
            col12.markdown(routine.EndTime)

            # Editar usuário
            if "rpa_edit_routine_id" in st.session_state:
                if st.session_state.get("rpa_edit_routine_id") == routine.Id:
                    routine_id = routine.Id
                    with st.form("rpa_edit_routine_form", width=1200):
                        st.subheader(f"Editar Rotina: {routine.RoutineName}")
                        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
                        with col1:
                            routine_description = st.text_area(label="Descrição da Rotina", value=routine.RoutineDescription, height=140)
                            enabled = st.selectbox(label="Ativo", options=list(dict_boolean_list.keys()), index=list(dict_boolean_list.values()).index(routine.Enabled), key="rpa_edit_routine_enabled")
                        with col2:
                            beginning_date = st.date_input(label="Data Inicial", value=dt.datetime.strptime(routine.Beginning, "%d/%m/%Y"), format="DD/MM/YYYY", key="rpa_edit_routine_beginning_date")
                            with_end_date = st.checkbox(label="Com data Final", value=False if routine.End is None else True, key="rpa_edit_routine_with_end_date")
                            end_date = st.date_input(label="Data Final", value=None if routine.End is None else dt.datetime.strptime(routine.End, "%d/%m/%Y"), format="DD/MM/YYYY", key="rpa_edit_routine_end_date")
                        with col3:
                            frequency_description = st.selectbox(label="Frequência", options=list(dict_schedule_frequency_list.keys()), index=list(dict_schedule_frequency_list.keys()).index(routine.FrequencyDescription), key="rpa_edit_routine_frequency_description")
                            recurrence_time = st.number_input(label="Intervalo da Recorrência", value=routine.RecurrenceTime, key="rpa_edit_routine_recurrence_time")
                            recurrence_description = st.selectbox(label="Recorrência", options=list(dict_schedule_recurrence_list.keys()), index=list(dict_schedule_recurrence_list.keys()).index(routine.RecurrenceDescription), key="rpa_edit_routine_recurrence_description")
                        with col4:
                            # star_time = st.time_input(label="Hora de Início", value=dt.datetime.strptime(routine.StartTime, "%H:%M:%S"), key="rpa_edit_routine_star_time")
                            # end_time = st.time_input(label="Hora de Término", value=dt.datetime.strptime(routine.EndTime, "%H:%M:%S"), key="rpa_edit_routine_end_time")
                            star_time = st.selectbox(label="Hora de Início", options=list(dict_hour_list.keys()), index=list(dict_hour_list.keys()).index(routine.StartTime), key="rpa_edit_routine_star_time")
                            end_time = st.selectbox(label="Hora de Término", options=list(dict_hour_list.keys()), index=list(dict_hour_list.keys()).index(routine.EndTime), key="rpa_edit_routine_end_time")

                        col1, col2, col3 = st.columns([3, 2, 12])
                        with col1:
                            bt_rpa_edit_routine_form_save_changes = st.form_submit_button("Salvar Alterações", use_container_width=True)
                        with col2:
                            bt_rpa_edit_routine_form_cancel = st.form_submit_button("Cancelar", use_container_width=True)

                        placeholder_rpa_edit_routine_form = st.empty()

                    # Salvar Alterações
                    if bt_rpa_edit_routine_form_save_changes:
                        try:
                            recurrence_time = abs(recurrence_time)
                            with engine_pd.begin() as conn:
                                rpa_edit_routine_update_query = sa.text(f"""
                                    UPDATE Nexus.rpa.[Routine]
                                        SET
                                            RoutineDescription = '{routine_description}'
                                            ,[Enabled] = {"1" if enabled == "Sim" else "0"}
                                        WHERE
                                            Id = {routine_id}
                                    ;
                                    UPDATE Nexus.rpa.[Schedule]
                                        SET
                                            Beginning = '{beginning_date.strftime("%Y-%m-%d")}'
                                            ,[End] = {"NULL" if not with_end_date else f"'{end_date.strftime("%Y-%m-%d")}'"}
                                            ,RecurrenceTime = {recurrence_time}
                                            ,FrequencyId = {dict_schedule_frequency_list.get(frequency_description)}
                                            ,RecurrenceId = {dict_schedule_recurrence_list.get(recurrence_description)}
                                            ,StartTime = '{star_time}'
                                            ,EndTime = '{end_time}'
                                        WHERE
                                            RoutineId = {routine_id}
                                    ;
                                """)
                                # st.write(rpa_edit_routine_update_query)
                                conn.execute(rpa_edit_routine_update_query)

                            if "rpa_edit_routine_id" in st.session_state:
                                del st.session_state["rpa_edit_routine_id"]
                            # placeholder_rpa_edit_routine_form.success("Rotina atualizada com sucesso.")
                            # time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            placeholder_rpa_edit_routine_form.error(e)
                            st.stop()

                    # Cancelar
                    elif bt_rpa_edit_routine_form_cancel:
                        if "rpa_edit_routine_id" in st.session_state:
                            del st.session_state["rpa_edit_routine_id"]
                        st.rerun()

                    # if "rpa_edit_routine_id" in st.session_state:
                    #     del st.session_state["rpa_edit_routine_id"]