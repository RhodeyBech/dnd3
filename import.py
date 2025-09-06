import re
import json
import pandas       as pd
import sqlalchemy   as sa

def convert_tables_to_json(text: str) -> str:
    if not text:
        return text

    # regex para encontrar tabelas markdown
    table_pattern = re.compile(r"(?:\|.+\|\n?)+")
    
    def table_replacer(match):
        table_text = match.group(0).strip()
        rows = [r.strip() for r in table_text.splitlines() if r.strip()]
        parsed_rows = [ [c.strip() for c in r.strip('|').split('|')] for r in rows ]
        
        header = parsed_rows[0]
        data_rows = parsed_rows[1:]
        table_json = [dict(zip(header, row)) for row in data_rows]
        
        return "{{json:" + json.dumps(table_json, ensure_ascii=False) + "}}"
    
    return table_pattern.sub(table_replacer, text)


magic_file_path = r"C:\Users\rodri\Google Drive\rhodeybech\tb_MAGIAS.xlsx"
source_file_path = r"C:\Users\rodri\Google Drive\rhodeybech\tb_FONTES.xlsx"
domain_file_path = r"C:\Users\rodri\Google Drive\rhodeybech\tb_DOMINIOS.xlsx"
set_extri_magic_file_path = r"C:\Users\rodri\Google Drive\rhodeybech\tb_DISTRIBUICAO_EXTRA_MAGIAS.xlsx"


df_magic = pd.read_excel(magic_file_path)
df_magic["DESCRICAO"] = df_magic["DESCRICAO"].apply(convert_tables_to_json)

# %26 no lugar de &
engine = sa.create_engine("mssql+pyodbc://sa:Craft3.5%26@RODRIGO-LAPTOP/DND3?driver=ODBC+Driver+17+for+SQL+Server")

df_magic.to_sql(
    name="Magic"
    ,schema="core"
    ,con=engine
    ,if_exists="append"
    ,index=False
)