import os
import pyarrow.parquet as pq
import pyarrow.compute as pc
import pyarrow as pa
import pandas as pd

# Configuração
PASTA = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2024"

ARQ_ACIDENTES   = os.path.join(PASTA, "acidentes_consolidado_2024.parquet")
ARQ_LOCALIDADES = os.path.join(PASTA, "localidades_consolidado_2024.parquet")
ARQ_SAIDA       = os.path.join(PASTA, "localidades_consolidado_filtrado_2024.parquet")

# ----------------------------------------------------------
# 1. Obter combinações únicas (chv_localidade + ano) dos acidentes
# ----------------------------------------------------------
print("📂 Lendo chaves de acidentes...")
tabela_ac = pq.read_table(ARQ_ACIDENTES, columns=['chv_localidade', 'ano_acidente'])
df_ac = tabela_ac.to_pandas()

# Cria conjunto de pares únicos
pares_ac = set(zip(df_ac['chv_localidade'], df_ac['ano_acidente']))
print(f"   Combinações únicas (chv + ano) nos acidentes: {len(pares_ac):,}")

# ----------------------------------------------------------
# 2. Carregar localidades completas
# ----------------------------------------------------------
print("📂 Lendo localidades completas...")
tabela_loc = pq.read_table(ARQ_LOCALIDADES)
# Garantimos que as colunas estejam na ordem esperada
colunas_loc = tabela_loc.column_names
print(f"   Localidades carregadas: {tabela_loc.num_rows:,}")

# ----------------------------------------------------------
# 3. Filtrar localidades – mantém apenas as combinações presentes nos acidentes
# ----------------------------------------------------------
# Converter para pandas para facilitar o filtro (a tabela é pequena, < 500k linhas)
df_loc = tabela_loc.to_pandas()
# Renomeia para compatibilidade no merge (faremos via isin com tuplas)
df_loc['par'] = list(zip(df_loc['chv_localidade'], df_loc['ano_referencia']))
mask = df_loc['par'].isin(pares_ac)
df_filtrado = df_loc[mask].drop(columns=['par'])

print(f"   Localidades antes: {len(df_loc):,}")
print(f"   Localidades referenciadas: {len(df_filtrado):,}")

# Remove eventuais duplicatas (garantia extra)
df_filtrado = df_filtrado.drop_duplicates()
print(f"   Únicas (após drop_duplicates): {len(df_filtrado):,}")

# ----------------------------------------------------------
# 4. Salvar
# ----------------------------------------------------------
print(f"💾 Salvando em {ARQ_SAIDA}...")
df_filtrado.to_parquet(ARQ_SAIDA, index=False)
print("✅ Arquivo de localidades filtrado criado com sucesso.")