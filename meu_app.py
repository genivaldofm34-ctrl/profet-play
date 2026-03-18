# Garantir cópia limpa
df_editado = df_editado.copy()

colunas = df_editado.columns.tolist()

col_nome = colunas[0]
col_total = colunas[-1]
cols_para_somar = colunas[1:-1]

# Converter tudo para número corretamente
df_editado[cols_para_somar] = df_editado[cols_para_somar].apply(
    pd.to_numeric, errors='coerce'
).fillna(0)

# Soma linha a linha
df_editado[col_total] = df_editado[cols_para_somar].sum(axis=1)
