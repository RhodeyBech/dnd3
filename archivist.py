import subprocess
import threading
import functions    as fn

fn.load_sidebar()

def run_streamlit():
    subprocess.run([
        "streamlit"
        ,"run"
        ,"--client.showSidebarNavigation=False"
        ,"--server.port=8501"
        ,"app.py"
    ])

threading.Thread(target=run_streamlit).start()