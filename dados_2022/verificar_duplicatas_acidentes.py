import os
import hashlib
from collections import defaultdict

PASTA_2024 = r"C:\Users\Programa\Desktop\DataFriend\RAW\Conjunto Extraído\2024"

def md5_arquivo(caminho):
    """Retorna o hash MD5 de um arquivo."""
    hash_md5 = hashlib.md5()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(8192), b""):
            hash_md5.update(bloco)
    return hash_md5.hexdigest()

# Coletar arquivos de acidentes
arquivos_acidentes = []
for arq in os.listdir(PASTA_2024):
    if not arq.endswith('.csv'):
        continue
    partes = arq.split(" - ", 1)
    if len(partes) == 2:
        prefixo, resto = partes
        if prefixo.strip().isdigit() and resto.startswith("Acidentes"):
            arquivos_acidentes.append(arq)

print(f"📂 {len(arquivos_acidentes)} arquivos de Acidentes encontrados em 2024.\n")

# Calcular hashes
hashes = defaultdict(list)
for arq in sorted(arquivos_acidentes):
    caminho = os.path.join(PASTA_2024, arq)
    h = md5_arquivo(caminho)
    hashes[h].append(arq)

# Exibir duplicatas
print("=" * 60)
print("RESULTADOS")
print("=" * 60)
grupos_duplicados = 0
for h, lista in hashes.items():
    if len(lista) > 1:
        grupos_duplicados += 1
        print(f"\n🔹 Hash: {h[:16]}...")
        print(f"   Arquivos idênticos ({len(lista)}):")
        for nome in lista:
            print(f"      - {nome}")

unicos = sum(1 for lst in hashes.values() if len(lst) == 1)
print(f"\n📊 Total de hashes distintos: {len(hashes)}")
print(f"   Arquivos únicos: {unicos}")
print(f"   Grupos de duplicatas: {grupos_duplicados}")