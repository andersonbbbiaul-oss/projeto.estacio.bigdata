import pandas as pd
import os

PASTA_2022 = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2022"
PASTA_2023 = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2023"

# Carregar apenas colunas de data
df_2022 = pd.read_parquet(
    os.path.join(PASTA_2022, "acidentes_consolidado.parquet"),
    columns=['ano_acidente', 'mes_acidente']
)
df_2023 = pd.read_parquet(
    os.path.join(PASTA_2023, "acidentes_consolidado_2023.parquet"),
    columns=['ano_acidente', 'mes_acidente']
)

# Totais por ano
anos_2022 = df_2022['ano_acidente'].value_counts().sort_index()
anos_2023 = df_2023['ano_acidente'].value_counts().sort_index()

# Totais por mês (todos os anos)
meses_2022 = df_2022['mes_acidente'].value_counts().sort_index()
meses_2023 = df_2023['mes_acidente'].value_counts().sort_index()

print("=" * 70)
print("COMPARAÇÃO DE ACIDENTES POR ANO (2022 vs 2023)")
print("=" * 70)
print(f"{'Ano':<10} {'2022':<12} {'2023':<12} {'Diferença':<12}")
for ano in sorted(set(anos_2022.index) | set(anos_2023.index)):
    v22 = anos_2022.get(ano, 0)
    v23 = anos_2023.get(ano, 0)
    diff = v23 - v22
    print(f"{ano:<10} {v22:<12,} {v23:<12,} {diff:<+12,}")

print("\n" + "=" * 70)
print("COMPARAÇÃO DE ACIDENTES POR MÊS (todos os anos)")
print("=" * 70)
print(f"{'Mês':<10} {'2022':<12} {'2023':<12} {'Diferença':<12}")
for mes in range(1, 13):
    v22 = meses_2022.get(mes, 0)
    v23 = meses_2023.get(mes, 0)
    diff = v23 - v22
    print(f"{mes:<10} {v22:<12,} {v23:<12,} {diff:<+12,}")