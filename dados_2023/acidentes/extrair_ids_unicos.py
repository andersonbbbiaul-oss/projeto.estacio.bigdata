import os
import pyarrow.csv as csv
import pyarrow.parquet as pq
import pyarrow as pa
from tqdm import tqdm

# Configuração
PASTA_RAW = r"C:\Users\Programa\Desktop\DataFriend\RAW\Conjunto Extraído\2023"
PASTA_SAIDA = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2023"
os.makedirs(PASTA_SAIDA, exist_ok=True)

ARQUIVO_FONTE = os.path.join(PASTA_RAW, "1 - Acidentes_DadosAbertos.csv")
ARQUIVO_SAIDA = os.path.join(PASTA_SAIDA, "ids_unicos_acidentes_2023.parquet")

ENCODING = 'latin1'
SEPARADOR = ';'

print(f"📂 Lendo arquivo: {ARQUIVO_FONTE}")
# Configura a leitura apenas da coluna 'num_acidente'
read_options = csv.ReadOptions(encoding=ENCODING)
parse_options = csv.ParseOptions(delimiter=SEPARADOR)
convert_options = csv.ConvertOptions(include_columns=['num_acidente'])

# Lê o CSV
tabela = csv.read_csv(
    ARQUIVO_FONTE,
    read_options=read_options,
    parse_options=parse_options,
    convert_options=convert_options
)

# Extrai IDs únicos (usando set para garantir unicidade)
print("🔍 Extraindo IDs únicos...")
ids = set()
for batch in tqdm(tabela.to_batches(max_chunksize=1_000_000), desc="Processando batches"):
    ids_batch = batch.column('num_acidente').to_pylist()
    ids.update(ids_batch)

print(f"   IDs únicos encontrados: {len(ids):,}")

# Cria tabela PyArrow com a coluna 'num_acidente'
tabela_ids = pa.table({'num_acidente': pa.array(list(ids), type=pa.int64())})

# Salva em Parquet
print(f"💾 Salvando em {ARQUIVO_SAIDA}...")
pq.write_table(tabela_ids, ARQUIVO_SAIDA, compression='snappy')
print("✅ Arquivo de IDs únicos criado com sucesso.")