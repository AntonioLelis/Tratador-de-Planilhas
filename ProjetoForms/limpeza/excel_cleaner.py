import pandas as pd

def carregar_excel(caminho):
    return pd.read_excel(caminho, header=None)

def limpar_excel(df, linha_header):
    df.columns = df.iloc[linha_header]
    df = df.drop(index=range(linha_header + 1))

    df = df.dropna(axis=1, how='all')
    df = df.dropna(axis=0, how='all')
    df = df.loc[:, ~df.columns.astype(str).str.contains('^Unnamed')]

    df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]

    return df.reset_index(drop=True)

def detectar_colunas_inconsistentes(df):
    inconsistentes = []
    for col in df.columns:
        tipos = df[col].dropna().map(type).nunique()
        if tipos > 1 or df[col].isna().sum() / len(df) > 0.5:
            inconsistentes.append(col)
    return inconsistentes