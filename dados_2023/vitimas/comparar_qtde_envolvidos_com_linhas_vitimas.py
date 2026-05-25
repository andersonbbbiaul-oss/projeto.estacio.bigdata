import os
import pyarrow.parquet as pq
import pyarrow.compute as pc

PASTA = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2023"
ARQ_ACIDENTES = os.path.join(PASTA, "acidentes_consolidado_2023.parquet")
ARQ_VITIMAS   = os.path.join(PASTA, "vitimas_consolidado_2023.parquet")

# 1. Somar qtde_envolvidos nos acidentes
print("📂 Lendo qtde_envolvidos dos acidentes...")
tabela_ac = pq.read_table(ARQ_ACIDENTES, columns=['qtde_envolvidos'])
soma_envolvidos = pc.sum(tabela_ac.column('qtde_envolvidos')).as_py()
print(f"   Soma de qtde_envolvidos: {soma_envolvidos:,}")

# 2. Contar linhas de vítimas
print("📂 Contando linhas de vítimas...")
meta_vit = pq.read_metadata(ARQ_VITIMAS)
total_vitimas = meta_vit.num_rows
print(f"   Total de linhas em Vítimas: {total_vitimas:,}")

# 3. Comparação
print("\n🔍 Comparação:")
print(f"   qtde_envolvidos (acidentes) = {soma_envolvidos:,}")
print(f"   linhas em vítimas            = {total_vitimas:,}")
if soma_envolvidos == total_vitimas:
    print("✅ Os valores são idênticos!")
else:
    diff = abs(soma_envolvidos - total_vitimas)
    perc = diff / soma_envolvidos * 100
    print(f"⚠️  Diferença: {diff:,} ({perc:.2f}% do total de envolvidos)")