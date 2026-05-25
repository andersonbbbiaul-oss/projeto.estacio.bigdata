import pandas as pd
import os

PASTA = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2023"
ARQ_ACIDENTES = os.path.join(PASTA, "acidentes_consolidado_2023.parquet")
ARQ_VEICULOS  = os.path.join(PASTA, "veiculos_consolidado_2023.parquet")
ARQ_ORFAOS    = os.path.join(PASTA, "veiculos_orfãos_2023.parquet")

print("📂 Carregando IDs de acidentes...")
df_ac = pd.read_parquet(ARQ_ACIDENTES, columns=['num_acidente'])
ids_validos = set(df_ac['num_acidente'])

print("📂 Carregando veículos...")
df_ve = pd.read_parquet(ARQ_VEICULOS)

# Filtra veículos cujo num_acidente NÃO está em acidentes
mask_orfãos = ~df_ve['num_acidente'].isin(ids_validos)
df_orfãos = df_ve[mask_orfãos]

print(f"\n🔍 Total de veículos: {len(df_ve):,}")
print(f"   Veículos com acidente válido: {(~mask_orfãos).sum():,}")
print(f"   Veículos ÓRFÃOS (sem acidente): {len(df_orfãos):,}")

# Salva os órfãos (mesmo que vazio, para manter consistência)
df_orfãos.to_parquet(ARQ_ORFAOS, index=False)
print(f"💾 Órfãos salvos em: {ARQ_ORFAOS}")