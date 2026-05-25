import os
import pyarrow.csv as csv

# Configuração
PASTA_2022 = r"C:\Users\Programa\Desktop\DataFriend\RAW\Conjunto Extraído\2022"
ENCODING   = 'latin1'
SEPARADOR  = ';'
MESES_ORDEM = [9, 8, 7, 6, 5, 4, 2, 1]  # do mais recente ao mais antigo (únicos restantes)

ids_unicos = set()

print("🔍 Análise progressiva dos arquivos de acidentes de 2022 (do mais recente ao mais antigo):\n")
for mes in MESES_ORDEM:
    prefixo = f"{mes} -"
    arquivos = [f for f in os.listdir(PASTA_2022) if f.startswith(prefixo) and 'Acidentes' in f]
    if not arquivos:
        print(f"   ⚠️ Nenhum arquivo para mês {mes}. Pulando.")
        continue

    caminho = os.path.join(PASTA_2022, arquivos[0])
    print(f"📄 Mês {mes:2d} – {arquivos[0]}")

    # Lê apenas a coluna 'num_acidente'
    read_options = csv.ReadOptions(encoding=ENCODING)
    parse_options = csv.ParseOptions(delimiter=SEPARADOR)
    convert_options = csv.ConvertOptions(include_columns=['num_acidente'])
    tabela = csv.read_csv(caminho, read_options=read_options,
                          parse_options=parse_options, convert_options=convert_options)

    ids_arquivo = set(tabela.column('num_acidente').to_pylist())
    novos = ids_arquivo - ids_unicos
    comuns = ids_arquivo & ids_unicos

    print(f"   Total de IDs no arquivo: {len(ids_arquivo):,}")
    print(f"   IDs já conhecidos: {len(comuns):,}")
    print(f"   IDs NOVOS (ainda não vistos): {len(novos):,}")

    if novos:
        print(f"   Exemplos de novos IDs: {sorted(list(novos))[:10]}")
    else:
        print("   Nenhum ID novo – esse arquivo é totalmente coberto pelos anteriores (mais recentes).")

    ids_unicos.update(novos)
    print()

print(f"✅ Total de IDs únicos acumulados após todos os arquivos: {len(ids_unicos):,}")