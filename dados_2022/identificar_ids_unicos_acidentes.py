import os
import pyarrow.csv as csv
import pyarrow.parquet as pq
import pyarrow as pa
from tqdm import tqdm

# Configuração
PASTA_RAW   = r"C:\Users\Programa\Desktop\DataFriend\RAW\Conjunto Extraído\2024"
PASTA_SAIDA = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2024"
os.makedirs(PASTA_SAIDA, exist_ok=True)

ARQUIVO_SAIDA = os.path.join(PASTA_SAIDA, "ids_unicos_acidentes_2024.parquet")
ENCODING      = 'latin1'
SEPARADOR     = ';'
MESES_ORDEM   = [12, 11, 10, 9, 8, 7, 6, 1]   # do mais recente ao mais antigo (sem 2,3,4,5 que eram duplicatas)

ids_unicos = set()
total_adicionados = 0

print("🔍 Extraindo IDs únicos de acidentes (processando do arquivo mais recente ao mais antigo)...")
for mes in MESES_ORDEM:
    prefixo = f"{mes} -"
    arquivos = [f for f in os.listdir(PASTA_RAW) if f.startswith(prefixo) and 'Acidentes' in f]
    if not arquivos:
        print(f"   ⚠️ Nenhum arquivo para mês {mes}. Pulando.")
        continue

    caminho = os.path.join(PASTA_RAW, arquivos[0])
    print(f"📄 Processando: {arquivos[0]}")

    # Lê apenas a coluna num_acidente
    read_options   = csv.ReadOptions(encoding=ENCODING)
    parse_options  = csv.ParseOptions(delimiter=SEPARADOR)
    convert_options = csv.ConvertOptions(include_columns=['num_acidente'])
    tabela = csv.read_csv(caminho, read_options=read_options,
                          parse_options=parse_options, convert_options=convert_options)

    # Obtém todos os IDs do arquivo e filtra os que ainda não foram vistos
    ids_arquivo = tabela.column('num_acidente').to_pylist()
    ids_novos = [id_ for id_ in ids_arquivo if id_ not in ids_unicos]
    if ids_novos:
        ids_unicos.update(ids_novos)
        total_adicionados += len(ids_novos)
        print(f"   → {len(ids_novos):,} IDs novos adicionados.")
    else:
        print("   → Nenhum ID novo encontrado.")

# Salva o resultado
print(f"\n💾 Salvando {len(ids_unicos):,} IDs únicos em {ARQUIVO_SAIDA}...")
tabela_ids = pa.table({'num_acidente': pa.array(list(ids_unicos), type=pa.int64())})
pq.write_table(tabela_ids, ARQUIVO_SAIDA, compression='snappy')
print("✅ Arquivo de IDs únicos criado com sucesso.")