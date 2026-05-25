import os
import pandas as pd
import pyarrow.parquet as pq

PASTA = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2025"

ARQ_ACIDENTES   = os.path.join(PASTA, "acidentes_consolidado_2025.parquet")
ARQ_LOCALIDADES = os.path.join(PASTA, "localidades_consolidado_2025.parquet")
ARQ_SAIDA       = os.path.join(PASTA, "localidades_consolidado_filtrado_2025.parquet")

# 1. Obter combinações únicas (chv_localidade + ano) dos acidentes
print("📂 Lendo chaves de acidentes...")
df_ac = pd.read_parquet(ARQ_ACIDENTES, columns=['chv_localidade', 'ano_acidente'])
pares_ac = set(zip(df_ac['chv_localidade'], df_ac['ano_acidente']))
print(f"   Combinações únicas nos acidentes: {len(pares_ac):,}")

# 2. Carregar localidades completas
print("📂 Lendo localidades completas...")
df_loc = pd.read_parquet(ARQ_LOCALIDADES)
print(f"   Localidades carregadas: {len(df_loc):,}")

# 3. Filtrar
df_loc['par'] = list(zip(df_loc['chv_localidade'], df_loc['ano_referencia']))
mask = df_loc['par'].isin(pares_ac)
df_filtrado = df_loc[mask].drop(columns=['par'])

print(f"   Localidades antes: {len(df_loc):,}")
print(f"   Localidades referenciadas: {len(df_filtrado):,}")

df_filtrado = df_filtrado.drop_duplicates()
print(f"   Únicas após drop_duplicates: {len(df_filtrado):,}")

# 4. Salvar
df_filtrado.to_parquet(ARQ_SAIDA, index=False)
print(f"✅ Arquivo de localidades filtrado criado com sucesso.")