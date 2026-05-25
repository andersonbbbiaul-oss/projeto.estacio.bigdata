import pandas as pd
import os

PASTA = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2024"
ARQUIVO = os.path.join(PASTA, "vitimas_consolidado_2024.parquet")

print("📂 Lendo arquivo de vítimas...")
df = pd.read_parquet(ARQUIVO)
print(f"   Total de linhas: {len(df):,}")

# Verifica duplicatas exatas (todas as colunas)
dup_exata = df.duplicated(keep=False)
num_dup = dup_exata.sum()

print("\n📄 Verificação de duplicatas exatas (todas as colunas iguais):")
if num_dup == 0:
    print("✅ Nenhuma linha duplicada.")
else:
    print(f"❌ Existem {num_dup:,} linhas idênticas.")
    exemplos = df[dup_exata].head(10)
    print("Exemplos de duplicatas (primeiras 10):")
    print(exemplos.to_string())

print("\n✅ Verificação concluída.")