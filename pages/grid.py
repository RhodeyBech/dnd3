# Rodrigo Bechara 06/09/2025
# Página de Campo
import streamlit as st
import streamlit.components.v1 as components

# Import local pasta anterior
import sys
sys.path.append("...")
import functions                as fn

# Oculta menu padrão de navegação do Streamlit
st.markdown("""
    <style>
        div[data-testid="stSidebarNav"] {chr(123)}display: none;{chr(125)}
    </style>
""", unsafe_allow_html=True)

# Identifica se o usuário está logado
if not st.session_state.get("is_logged", False):
    st.switch_page("pages/login.py")

# Configuração da página
st.set_page_config(
    page_title="Archivist"
    ,page_icon=""
    ,layout="wide"
)

# Ajusta cabeçalho da página
fn.hidden_header()

# Define página ativa
st.session_state["active_page"] = "grid"

# Carrega a barra lateral
fn.load_sidebar()

# Título
st.subheader("Campo")

components.html(f"""
    <style>
        .grid {chr(123)}
        display: grid;
        grid-template-columns: repeat(3, 100px);
        grid-template-rows: repeat(3, 100px);
        gap: 0.5px;
    {chr(125)}
    .cell {chr(123)}
        width: 100px;
        height: 100px;
        border: 2px solid #333;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: {"#f5f5f5"};
    {chr(125)}
    .draggable {chr(123)}
        width: 80px;
        height: 80px;
        background-color: {"#4caf50"};
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: grab;
        user-select: none;
    {chr(125)}
    </style>

    <div class="grid">
    <div class="cell" id="cell-0"></div>
    <div class="cell" id="cell-1">
        <div class="draggable" draggable="true" id="obj-1">Obj 1</div>
    </div>
    <div class="cell" id="cell-2"></div>
    <div class="cell" id="cell-3"></div>
    <div class="cell" id="cell-4"></div>
    <div class="cell" id="cell-5"></div>
    <div class="cell" id="cell-6"></div>
    <div class="cell" id="cell-7"></div>
    <div class="cell" id="cell-8"></div>
    </div>

    <script>
    document.addEventListener('DOMContentLoaded', () => {chr(123)}
    const cells = document.querySelectorAll('.cell');
    const draggables = document.querySelectorAll('.draggable');

    draggables.forEach(drag => {chr(123)}
        drag.addEventListener('dragstart', ev => {chr(123)}
        ev.dataTransfer.setData("text/plain", ev.target.id);
        {chr(125)});
    {chr(125)});

    cells.forEach(cell => {chr(123)}
        cell.addEventListener('dragover', ev => ev.preventDefault());
        cell.addEventListener('drop', ev => {chr(123)}
        ev.preventDefault();
        const id = ev.dataTransfer.getData("text/plain");
        const dragged = document.getElementById(id);
        if (cell.children.length === 0) {chr(123)}
            cell.appendChild(dragged);
        {chr(125)}
        {chr(125)});
    {chr(125)});
    {chr(125)});
    </script>
""", height=350)