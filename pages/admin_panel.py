# Rodrigo Bechara 15/07/2025
# Página de administração de usuários
import streamlit                as st
import functions                as fn
import sqlalchemy               as sa
import time

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

# Proteger acesso
if st.session_state.get("access_level_id") > 2:
    st.switch_page("pages/home.py")

# Ajusta cabeçalho da página
fn.hidden_header()

# Configuração da página
st.set_page_config(
    page_title="Nexus"
    ,page_icon="https://www.csg.com.br/build/assets/favicon-c752c7b3.png"
    ,layout="wide"
)

# Define página ativa
st.session_state["active_page"] = "admin_panel"

# Carrega a barra lateral
fn.load_sidebar()

# Título
st.subheader("Painel Administrativo")

# Atualiza usuário conectado
fn.reload_active_user()

engine_pd = fn.get_pd_connection()

# Buscar níveis de acesso
with engine_pd.connect() as conn:
    # Administrador
    if st.session_state.get("access_level_id") == 1:
        levels_str = "Id >= 1"
    # Gestor
    elif st.session_state.get("access_level_id") == 2:
        levels_str = "Id = 3"

    levels_query = sa.text(f"""
        SELECT
            Id
            ,[Description]
        FROM Nexus.auth.AccessLevels
        WHERE
            {levels_str}
        ORDER BY
            [Description]
        """)
    levels = conn.execute(levels_query).fetchall()
    level_options = {l.Description: l.Id for l in levels}

# Buscar grupos
with engine_pd.connect() as conn:
    # 1 - Administração
    # 2 - Teste de Software
    # 3 - Geral
    # 4 - Diretoria
    # 5 - Backoffice
    # 6 - Financeiro
    # 7 - TI
    # 8 - Comunicação
    # 9 - Gestão de Pessoas
    # Administrador
    if st.session_state.get("group_id") == 1 or st.session_state.get("access_level_id") == 1:
        groups_str = f"Id >= 1"
    # Testador
    elif st.session_state.get("group_id") == 2:
        groups_str = f"Id >= 2"
    # Gestor
    elif st.session_state.get("access_level_id") == 2:
        groups_str = f"Id IN (3, {st.session_state.get("group_id")})"

    groups_query = sa.text(f"""
        SELECT
            Id
            ,[Description]
        FROM Nexus.auth.Groups
        WHERE
            {groups_str}
        ORDER BY
            [Description]
    """)
    groups = conn.execute(groups_query).fetchall()
    group_options = {g.Description: g.Id for g in groups}

# Cria abas
tab_user, = st.tabs(["Usuários"])

with tab_user:
    # Formulário de criação
    with st.form("create_user_form", width=700):
        st.subheader("Novo Usuário")

        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password", value="nexus@csg", disabled=True)
        group = st.selectbox("Grupo", options=list(group_options.keys()))
        access_level = st.selectbox("Nível de Acesso", options=list(level_options.keys()))
        is_active = st.checkbox("Ativo", value=True)
        if "@" in username:
            username = username.split("@")[0]

        submitted = st.form_submit_button("Criar Usuário")
        if submitted:
            if username != "":
                # Verifica se usuário existe
                with engine_pd.begin() as conn:
                    exists_query = sa.text("""
                        SELECT
                            1
                        FROM Nexus.auth.Users
                        WHERE
                            Username = :username
                    """)
                    exists_user = conn.execute(exists_query, {"username": username}).fetchone()

                if not exists_user:
                    hashed_password = fn.hash_password(password)
                    with engine_pd.begin() as conn:
                        query_create_user = sa.text(f"""
                            INSERT INTO Nexus.auth.Users (
                                Username
                                ,PasswordHash
                                ,GroupId
                                ,AccessLevelId
                                ,IsActive
                            )
                            VALUES (
                                '{username}'
                                ,'{hashed_password}'
                                ,{group_options[group]}
                                ,{level_options[access_level]}
                                ,{int(is_active)}
                            )
                        """)
                        conn.execute(query_create_user)
                    st.success("Usuário criado com sucesso.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Processo Cancelado. Já existe o usuário ''{username}''.")
            else:
                st.error(f"Nome de usuário inválido.")

    # Lista de usuários
    st.subheader("Usuários Cadastrados")
    with engine_pd.connect() as conn:
        groups_str = ""
        # Administração
        if st.session_state.get("group_id") == 1 or st.session_state.get("access_level_id") == 1:
            groups_str = "U.GroupId >= 1"
        # Teste de Software
        elif st.session_state.get("group_id") == 2:
            groups_str = f"""
                U.GroupId >= 2 AND U.GroupId <> 4
                AND U.AccessLevelId > {st.session_state.get("access_level_id")}
            """
        # Diretor
        elif st.session_state.get("group_id") == 4:
            groups_str = "U.GroupId >= 3"
        # Gestor
        elif st.session_state.get("group_id") >= 5:
            groups_str = f"""
                U.GroupId IN (3, {st.session_state.get("group_id")})
                AND U.AccessLevelId > {st.session_state.get("access_level_id")}
            """

        users = conn.execute(sa.text(f"""
            SELECT
                U.Id                    AS UserId
                ,U.Username
                ,U.IsActive
                ,G.Description          AS GroupDescription
                ,U.GroupId
                ,A.Description          AS AccessLevelDescription
                ,U.AccessLevelId
            FROM Nexus.auth.Users               AS U
            LEFT JOIN Nexus.auth.AccessLevels   AS A
                ON A.Id = U.AccessLevelId
            LEFT JOIN Nexus.auth.Groups         AS G
                ON G.Id = U.GroupId
            WHERE
                {groups_str}
            ORDER BY
                G.Description
                ,U.Username
        """)).fetchall()

        # Cabeçalho
        col1, col2, col3, col4, col5, col6, col7 = st.columns([14, 10, 10, 4, 1, 8, 12])
        col1.markdown("**— USUÁRIO (NÍVEL DE ACESSO) —**")
        col2.markdown("**— GRUPO —**")
        col3.markdown("**— ATIVO —**")
        col4.markdown("<div style='text-align: center; font-weight: 600;'>— EDIÇÃO —</div>", unsafe_allow_html=True)
        col6.markdown("<div style='text-align: center; font-weight: 600;'>— SENHA —</div>", unsafe_allow_html=True)

        # Cria tabela de dados
        last_group_id = ""
        for user in users:
            if last_group_id != "" and last_group_id != user.GroupId:
                fn.horizontal_divider()
            last_group_id = user.GroupId
            col1, col2, col3, col4, col5, col6, col7 = st.columns([14, 10, 10, 4, 1, 8, 12])
            col1.markdown(f"**{user.Username}** ({user.AccessLevelDescription})")
            col2.markdown(f"{user.GroupDescription}")
            status = "✅ Ativo" if user.IsActive else "❌ Inativo"
            col3.markdown(status)
            if col4.button("Editar", key=f"edit_{user.UserId}", use_container_width=True):
                st.session_state["edit_user_id"] = user.UserId
                if "reset_password_user_id" in st.session_state:
                    del st.session_state["reset_password_user_id"]
                st.rerun()
            if col6.button("Redefinir Senha", key=f"reset_password_{user.UserId}", use_container_width=True):
                st.session_state["reset_password_user_id"] = user.UserId
                st.session_state["reset_password_username"] = user.Username
                if "edit_user_id" in st.session_state:
                    del st.session_state["edit_user_id"]
                st.rerun()

            # Redefinir senha
            if "reset_password_user_id" in st.session_state:
                if st.session_state.get("reset_password_username") == user.Username:
                    with st.form("reset_password_form", width=700):
                        # Confirmação
                        st.markdown(f'##### Deseja redefinir a senha do usuário "{st.session_state.get("reset_password_username")}"?')

                        # Cria colunas
                        col1, col2, col3 = st.columns([1, 1, 4])
                        with col1:
                            bt_yes = st.form_submit_button("Sim", use_container_width=True)
                        with col2:
                            bt_no = st.form_submit_button("Não", use_container_width=True)

                        # Salvar Alterações
                        if bt_yes:
                            try:
                                with engine_pd.begin() as conn:
                                    update_query = sa.text("""
                                        UPDATE Nexus.auth.Users
                                            SET
                                                PasswordHash = :password
                                            WHERE
                                                Id = :uid
                                    """)
                                    conn.execute(update_query, {
                                        "uid": st.session_state.get("reset_password_user_id")
                                        ,"password": fn.hash_password("nexus@csg")
                                    })

                                st.success("Senha redefinida com sucesso.")
                                del st.session_state["reset_password_user_id"]
                                del st.session_state["reset_password_username"]
                                time.sleep(1)
                                st.rerun()
                            except Exception as e:
                                del st.session_state["reset_password_user_id"]
                                del st.session_state["reset_password_username"]
                                st.error(f"Erro ao atualizar usuário: {e}")
                        # Cancelar
                        elif bt_no:
                            del st.session_state["reset_password_user_id"]
                            del st.session_state["reset_password_username"]
                            st.rerun()

            # Editar usuário
            elif "edit_user_id" in st.session_state:
                if st.session_state.get("edit_user_id") == user.UserId:
                    with st.form("edit_user_form", width=700):
                        user_id = st.session_state.get("edit_user_id")

                        with engine_pd.connect() as conn:
                            user = conn.execute(sa.text("""
                                SELECT
                                    Username
                                    ,IsActive
                                    ,GroupId
                                    ,AccessLevelId
                                FROM Nexus.auth.Users
                                WHERE
                                    Id = :uid
                            """)
                            ,{"uid": user_id}).fetchone()

                        st.subheader(f"Editar Usuário: {user.Username.title().replace(".", " ")}")
                        new_group = st.selectbox("Grupo", options=list(group_options.keys()), index=list(group_options.values()).index(user.GroupId))
                        new_level = st.selectbox("Nível de Acesso", options=list(level_options.keys()), index=list(level_options.values()).index(user.AccessLevelId))
                        new_status = st.checkbox("Ativo", value=user.IsActive)

                        # Cria colunas
                        col1, col2, col3 = st.columns([3, 2, 6])
                        
                        with col1:
                            bt_save_changes = st.form_submit_button("Salvar Alterações", use_container_width=True)
                        with col2:
                            bt_cancel = st.form_submit_button("Cancelar", use_container_width=True)

                        # Salvar Alterações
                        if bt_save_changes:
                            try:
                                with engine_pd.begin() as conn:
                                    update_fields = "GroupId = :group_id, AccessLevelId = :access_level_id, IsActive = :is_active"
                                    params = {
                                        "uid": user_id
                                        ,"group_id": group_options[new_group]
                                        ,"access_level_id": level_options[new_level]
                                        ,"is_active": int(new_status)
                                    }
                                    update_query = sa.text(f"""
                                        UPDATE Nexus.auth.Users
                                            SET
                                                {update_fields}
                                            WHERE
                                                Id = :uid
                                    """)
                                    conn.execute(update_query, params)

                                st.success("Usuário atualizado com sucesso.")
                                if st.session_state.get("edit_user_id") == st.session_state.get("user_id"):
                                    # Atualiza usuário conectado
                                    fn.reload_active_user()

                                del st.session_state["edit_user_id"]
                                time.sleep(1)
                                st.rerun()
                            except Exception as e:
                                del st.session_state["edit_user_id"]
                                st.error(f"Erro ao atualizar usuário: {e}")

                        # Cancelar
                        elif bt_cancel:
                            del st.session_state["edit_user_id"]
                            st.rerun()

