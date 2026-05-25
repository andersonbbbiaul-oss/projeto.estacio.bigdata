import pandas as pd
import os

# Caminho do arquivo consolidado de veículos de 2024
PASTA = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2024"
ARQUIVO = os.path.join(PASTA, "veiculos_consolidado_2024.parquet")

print("📂 Lendo arquivo de veículos...")
df = pd.read_parquet(ARQUIVO)
print(f"   Total de linhas: {len(df):,}")

# 1. Duplicatas exatas (todas as colunas iguais)
dup_exata = df.duplicated(keep=False)
num_dup_exata = dup_exata.sum()

print("\n📄 Verificação de duplicatas exatas (todas as colunas iguais):")
if num_dup_exata == 0:
    print("✅ Nenhuma linha completamente duplicada.")
else:
    print(f"❌ Existem {num_dup_exata:,} linhas idênticas.")
    exemplos = df[dup_exata].head(10)
    print("Exemplos de duplicatas exatas (primeiras 10):")
    print(exemplos.to_string())

# 2. Duplicatas na chave composta (num_acidente + tipo_veiculo)
dup_chave = df.duplicated(subset=['num_acidente', 'tipo_veiculo'], keep=False)
num_dup_chave = dup_chave.sum()

print("\n🔑 Verificação de chave composta (num_acidente + tipo_veiculo):")
if num_dup_chave == 0:
    print("✅ Nenhuma duplicata na chave composta – cada par (acidente, tipo) é único.")
else:
    print(f"❌ Existem {num_dup_chave:,} linhas com o mesmo par (num_acidente, tipo_veiculo).")
    exemplos = df[dup_chave].head(10)
    print("Exemplos de duplicatas na chave (primeiras 10):")
    print(exemplos.to_string())

print("\n✅ Verificação concluída.")