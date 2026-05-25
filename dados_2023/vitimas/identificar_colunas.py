import os

PASTA_RAW = r"C:\Users\Programa\Desktop\DataFriend\RAW\Conjunto Extraído\2023"
ENCODING = 'latin1'
SEPARADOR = ';'

# Usa o primeiro arquivo de vítimas (todos são iguais)
arquivo = os.path.join(PASTA_RAW, "1 - Vitimas_DadosAbertos.csv")

with open(arquivo, 'r', encoding=ENCODING) as f:
    primeira_linha = f.readline().strip()

colunas = [col.strip() for col in primeira_linha.split(SEPARADOR)]

print(f"📄 Colunas do arquivo de Vítimas de 2023 ({len(colunas)}):")
for col in colunas:
    print(f"   - {col}")