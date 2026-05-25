import os
import hashlib
from collections import defaultdict

PASTA = r"C:\Users\Programa\Desktop\DataFriend\RAW\Conjunto Extraído\2023"

def md5_arquivo(caminho):
    hash_md5 = hashlib.md5()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(8192), b""):
            hash_md5.update(bloco)
    return hash_md5.hexdigest()

# Coletar arquivos de Localidade
arquivos_localidade = []
for arq in os.listdir(PASTA):
    if not arq.endswith('.csv'):
        continue
    partes = arq.split(" - ", 1)
    if len(partes) == 2:
        prefixo, resto = partes
        if prefixo.strip().isdigit() and resto.startswith("Localidade"):
            arquivos_localidade.append(arq)

print(f"📂 {len(arquivos_localidade)} arquivos de Localidade encontrados em 2023.\n")

# Calcular hashes
hashes = defaultdict(list)
for arq in sorted(arquivos_localidade):
    caminho = os.path.join(PASTA, arq)
    h = md5_arquivo(caminho)
    hashes[h].append(arq)

# Exibir resultados
print("=" * 60)
print("RESULTADOS")
print("=" * 60)
for h, lista in hashes.items():
    if len(lista) > 1:
        print(f"\n🔹 Hash: {h[:16]}...")
        print(f"   Arquivos idênticos ({len(lista)}):")
        for nome in lista:
            print(f"      - {nome}")

# Resumo
total_hashes = len(hashes)
unicos = sum(1 for lst in hashes.values() if len(lst) == 1)
grupos = sum(1 for lst in hashes.values() if len(lst) > 1)
print(f"\n📊 Total de hashes distintos: {total_hashes}")
print(f"   Arquivos únicos: {unicos}")
print(f"   Grupos de duplicatas: {grupos}")