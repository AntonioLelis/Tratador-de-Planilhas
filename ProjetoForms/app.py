import streamlit as st
import pandas as pd
import os
from limpeza.excel_cleaner import carregar_excel, limpar_excel, detectar_colunas_inconsistentes
from limpeza.pdf_extractor import extrair_tabelas_pdf

st.title("Organizador de Relatórios")

uploaded_file = st.file_uploader("Carregue um relatório (Excel ou PDF)", type=["xlsx", "pdf"])

if uploaded_file:
    caminho_entrada = os.path.join("entrada", uploaded_file.name)
    with open(caminho_entrada, "wb") as f:
        f.write(uploaded_file.read())

    if uploaded_file.name.endswith(".xlsx"):
        df_bruto = carregar_excel(caminho_entrada)
        st.subheader("Pré-visualização bruta do relatório")
        st.dataframe(df_bruto.head(10))

        linha_header = st.number_input("Selecione a linha do cabeçalho (0-indexado)", min_value=0, max_value=len(df_bruto)-1, step=1)
        if st.button("Limpar relatório"):
            df_limpo = limpar_excel(df_bruto, linha_header)
            col_inconsistentes = detectar_colunas_inconsistentes(df_limpo)

            st.subheader("✅ Relatório limpo")
            st.dataframe(df_limpo)

            if col_inconsistentes:
                st.warning(f"Colunas com dados inconsistentes ou muitos valores ausentes: {', '.join(col_inconsistentes)}")

            df_limpo.to_excel("saida/relatorio_limpo.xlsx", index=False, engine='xlsxwriter')
            with open("saida/relatorio_limpo.xlsx", "rb") as f:
                st.download_button(
                    label="📥 Baixar relatório limpo em Excel",
                    data=f,
                    file_name="relatorio_limpo.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    elif uploaded_file.name.endswith(".pdf"):
        st.info("Extraindo tabelas do PDF...")
        df = extrair_tabelas_pdf(caminho_entrada)
        st.subheader("Prévia da tabela extraída")
        st.dataframe(df.head())

        df.to_excel("saida/relatorio_limpo.xlsx", index=False, engine='xlsxwriter')
        with open("saida/relatorio_limpo.xlsx", "rb") as f:
            st.download_button(
                label="📥 Baixar tabela extraída do PDF",
                data=f,
                file_name="relatorio_limpo.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )