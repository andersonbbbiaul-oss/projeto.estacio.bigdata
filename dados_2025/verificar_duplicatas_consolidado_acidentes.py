import pandas as pd
import os

PASTA = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2025"
ARQUIVO = os.path.join(PASTA, "acidentes_consolidado_2025.parquet")

print("📂 Lendo arquivo...")
df = pd.read_parquet(ARQUIVO)
print(f"   Total de linhas: {len(df):,}")

# 1. Duplicatas na chave primária (num_acidente)
dup_chave = df.duplicated(subset='num_acidente', keep=False)
num_dup_chave = dup_chave.sum()

print("\n🔑 Verificação de chave primária (num_acidente):")
if num_dup_chave == 0:
    print("✅ Nenhuma duplicata de num_acidente – chave única.")
else:
    print(f"❌ Existem {num_dup_chave:,} linhas com num_acidente duplicado.")
    exemplos = df[dup_chave].head(10)
    print("Exemplos de linhas duplicadas (primeiras 10):")
    print(exemplos[['num_acidente']].to_string())

# 2. Duplicatas exatas de todas as colunas
dup_exata = df.duplicated(keep=False)
num_dup_exata = dup_exata.sum()

print("\n📄 Verificação de duplicatas exatas (todas as colunas):")
if num_dup_exata == 0:
    print("✅ Nenhuma linha completamente duplicada.")
else:
    print(f"❌ Existem {num_dup_exata:,} linhas idênticas (todas as colunas iguais).")
    exemplos = df[dup_exata].head(10)
    print("Exemplos de linhas duplicadas (primeiras 10):")
    print(exemplos.to_string())

print("\n✅ Verificação concluída.")