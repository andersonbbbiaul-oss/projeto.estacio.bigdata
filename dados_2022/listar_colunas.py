import os
import pyarrow.parquet as pq

PASTA = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2022"

arquivos = {
    "Acidentes":   "acidentes_consolidado_2022.parquet",
    "Localidades": "localidades_consolidado_2022.parquet",
    "Veículos":    "veiculos_consolidado_2022.parquet",
    "Vítimas":     "vitimas_consolidado_2022.parquet",
}

print("📄 Colunas de cada arquivo consolidado de 2022:\n")
for nome, arq in arquivos.items():
    caminho = os.path.join(PASTA, arq)
    if not os.path.exists(caminho):
        print(f"❌ {nome}: arquivo não encontrado ({arq})\n")
        continue
    schema = pq.read_schema(caminho)
    colunas = schema.names
    print(f"🔹 {nome} ({len(colunas)} colunas):")
    for col in colunas:
        print(f"   - {col}")
    print()