import os
import pyarrow.parquet as pq
import pandas as pd
import numpy as np

# Configuração
PASTA = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2023"
ARQUIVO = os.path.join(PASTA, "acidentes_consolidado_2023.parquet")

print("=" * 60)
print("VERIFICAÇÃO DE INTEGRIDADE – ACIDENTES 2023")
print("=" * 60)

# ----------------------------------------------------------
# 1. Metadados e contagem
# ----------------------------------------------------------
meta = pq.read_metadata(ARQUIVO)
schema = pq.read_schema(ARQUIVO)
colunas = [field.name for field in schema]
n_linhas = meta.num_rows

print(f"\n📏 Linhas: {n_linhas:,}")
print(f"📋 Colunas ({len(colunas)}): {colunas}")

# ----------------------------------------------------------
# 2. Unicidade de num_acidente
# ----------------------------------------------------------
print("\n🔑 Verificando unicidade de 'num_acidente'...")
tabela_ids = pq.read_table(ARQUIVO, columns=['num_acidente'])
ids = tabela_ids.column('num_acidente').to_pylist()
unicos = set(ids)
if len(ids) == len(unicos):
    print(f"✅ num_acidente é único: {len(ids):,} registros distintos.")
else:
    print(f"❌ num_acidente NÃO é único! Total={len(ids):,}, Únicos={len(unicos):,}")

# ----------------------------------------------------------
# 3. Nulos
# ----------------------------------------------------------
print("\n🔍 Verificando valores nulos...")
tabela = pq.read_table(ARQUIVO)
nulos_dict = {}
for col in colunas:
    null_count = tabela.column(col).null_count
    if null_count > 0:
        nulos_dict[col] = null_count
if nulos_dict:
    print("⚠️  Colunas com nulos:")
    for c, n in nulos_dict.items():
        print(f"   - {c}: {n:,}")
else:
    print("✅ Nenhum valor nulo encontrado.")

# ----------------------------------------------------------
# 4. Tipos de dados
# ----------------------------------------------------------
print("\n📊 Tipos de dados:")
for field in schema:
    print(f"   {field.name}: {field.type}")

# ----------------------------------------------------------
# 5. Valores de domínio esperados
# ----------------------------------------------------------
print("\n🌐 Verificando domínios...")
# Carrega DataFrame (como temos só 4.75M linhas, cabe na RAM)
df = pd.read_parquet(ARQUIVO)

# 5.1 ano_acidente
anos = sorted(df['ano_acidente'].unique())
print(f"   Anos encontrados: {anos}")
if all(2018 <= a <= 2023 for a in anos):
    print("   ✅ Anos dentro do intervalo 2018‑2023.")
else:
    print("   ⚠️  Anos fora do intervalo esperado.")

# 5.2 uf_acidente
ufs = df['uf_acidente'].unique()
print(f"   UFs ({len(ufs)}): {sorted(ufs)}")
if len(ufs) == 27:
    print("   ✅ 27 UFs presentes.")
else:
    print(f"   ⚠️  Número de UFs: {len(ufs)} (esperado 27).")

# 5.3 tp_acidente
tipos = df['tp_acidente'].unique()
print(f"   Tipos de acidente ({len(tipos)}):")
for t in sorted(tipos):
    print(f"      - {t}")

# 5.4 fase_dia
fases = sorted(df['fase_dia'].unique())
print(f"   Fases do dia: {fases}")

# 5.5 dia_semana
dias = sorted(df['dia_semana'].unique())
print(f"   Dias da semana: {dias}")

# 5.6 cond_meteorologica
condicoes = sorted(df['cond_meteorologica'].unique())
print(f"   Condições meteorológicas ({len(condicoes)}): {condicoes}")

# 5.7 mes_acidente
meses = sorted(df['mes_acidente'].unique())
print(f"   Meses: {meses}")
if meses == list(range(1,13)):
    print("   ✅ Todos os meses presentes.")
else:
    print("   ⚠️  Meses incompletos.")

# ----------------------------------------------------------
# 6. Duplicatas exatas de linhas
# ----------------------------------------------------------
print("\n🔁 Verificando duplicatas de linhas...")
dups = df.duplicated()
n_dups = dups.sum()
if n_dups == 0:
    print("✅ Nenhuma linha duplicada (todas as colunas iguais).")
else:
    print(f"❌ Existem {n_dups:,} linhas duplicadas (idênticas em todas as colunas).")
    # Se houver poucas, mostra exemplos
    if n_dups <= 20:
        print("   Exemplos de linhas duplicadas:")
        print(df[dups].head(10).to_string())

# ----------------------------------------------------------
# 7. Amostra
# ----------------------------------------------------------
print("\n📋 Amostra (5 primeiras linhas):")
print(df.head(5).to_string())

# ----------------------------------------------------------
# 8. Coerência básica entre data e mês
# ----------------------------------------------------------
print("\n📅 Verificando coerência data_acidente x mes_acidente...")
# Extrai mês da data (formato YYYY-MM-DD ou similar)
try:
    mes_da_data = pd.to_datetime(df['data_acidente']).dt.month
    batem = (mes_da_data == df['mes_acidente']).mean()
    print(f"   Coincidência: {batem:.4%}")
    if batem == 1.0:
        print("   ✅ Data e mês batem em 100% dos registros.")
    else:
        print("   ⚠️  Há divergências entre data e mês.")
except Exception as e:
    print(f"   ❌ Não foi possível verificar: {e}")

print("\n✅ Verificação concluída.")