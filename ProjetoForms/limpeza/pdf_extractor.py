import pdfplumber
import pandas as pd

def extrair_tabelas_pdf(caminho):
    tabelas = []
    with pdfplumber.open(caminho) as pdf:
        for pagina in pdf.pages:
            tabela = pagina.extract_table()
            if tabela:
                df = pd.DataFrame(tabela[1:], columns=tabela[0])
                tabelas.append(df)
    return pd.concat(tabelas, ignore_index=True)