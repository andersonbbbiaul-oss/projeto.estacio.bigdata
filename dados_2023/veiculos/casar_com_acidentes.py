import os
import pyarrow.csv as csv
import pyarrow.parquet as pq
import pyarrow.compute as pc
import pyarrow as pa
from tqdm import tqdm

# ----------------------------------------------------------
# Configuração
# ----------------------------------------------------------
PASTA_RAW   = r"C:\Users\Programa\Desktop\DataFriend\RAW\Conjunto Extraído\2023"
PASTA_SAIDA = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2023"
os.makedirs(PASTA_SAIDA, exist_ok=True)

ARQUIVO_IDS      = os.path.join(PASTA_SAIDA, "ids_unicos_acidentes_2023.parquet")
ARQUIVO_FONTE    = os.path.join(PASTA_RAW, "1 - TipoVeiculo_DadosAbertos.csv")
ARQUIVO_SAIDA    = os.path.join(PASTA_SAIDA, "veiculos_consolidado_2023.parquet")

ENCODING   = 'latin1'
SEPARADOR  = ';'
CHUNK_SIZE = 1_000_000   # linhas por batch para filtrar

# Colunas que queremos manter (mesmas de 2022)
COLUNAS = ['num_acidente', 'tipo_veiculo', 'qtde_veiculos']

# ----------------------------------------------------------
# 1. Carregar IDs únicos de acidentes
# ----------------------------------------------------------
print("📂 Carregando IDs únicos de acidentes...")
tabela_ids = pq.read_table(ARQUIVO_IDS, columns=['num_acidente'])
ids_unicos = set(tabela_ids.column('num_acidente').to_pylist())
print(f"   {len(ids_unicos):,} IDs carregados.\n")

# ----------------------------------------------------------
# 2. Ler CSV de veículos e filtrar
# ----------------------------------------------------------
print(f"📄 Processando: {os.path.basename(ARQUIVO_FONTE)}")

read_options   = csv.ReadOptions(encoding=ENCODING)
parse_options  = csv.ParseOptions(delimiter=SEPARADOR)
convert_options = csv.ConvertOptions(include_columns=COLUNAS)

# Abre o CSV em modo streaming (batches)
csv_reader = csv.open_csv(
    ARQUIVO_FONTE,
    read_options=read_options,
    parse_options=parse_options,
    convert_options=convert_options
)

# Lista para acumular DataFrames pandas (mais prático para filtro e escrita)
import pandas as pd
lista_dfs = []

# Barra de progresso para os batches
with tqdm(desc="   Filtrando veículos", unit=" batches") as pbar:
    for batch in csv_reader:
        table_batch = pa.Table.from_batches([batch])

        # Filtra apenas os num_acidente que estão no conjunto de IDs únicos
        mask = pc.is_in(
            table_batch.column('num_acidente'),
            value_set=pa.array(list(ids_unicos), type=pa.int64())
        )
        table_filtrada = table_batch.filter(mask)

        if table_filtrada.num_rows > 0:
            df_filtrado = table_filtrada.to_pandas()
            lista_dfs.append(df_filtrado)

        pbar.update(1)

# ----------------------------------------------------------
# 3. Concatenar e remover duplicatas (par (num_acidente, tipo_veiculo))
# ----------------------------------------------------------
print("\n🔄 Concatenando e removendo duplicatas...")
df_unido = pd.concat(lista_dfs, ignore_index=True)
linhas_antes = len(df_unido)

# Remove duplicatas mantendo a primeira ocorrência (como em 2022)
df_final = df_unido.drop_duplicates(subset=['num_acidente', 'tipo_veiculo'], keep='first')
print(f"   Linhas antes: {linhas_antes:,}")
print(f"   Linhas após deduplicação: {len(df_final):,}")

# ----------------------------------------------------------
# 4. Salvar
# ----------------------------------------------------------
print(f"\n💾 Salvando em {ARQUIVO_SAIDA}...")
df_final.to_parquet(ARQUIVO_SAIDA, index=False)
print("✅ Arquivo de veículos consolidado criado com sucesso.")