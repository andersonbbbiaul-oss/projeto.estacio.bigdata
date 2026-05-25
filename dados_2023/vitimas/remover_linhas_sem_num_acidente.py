import os
import pyarrow.parquet as pq
import pyarrow as pa
import pyarrow.compute as pc
from tqdm import tqdm

PASTA = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2023"

ARQ_IDS = os.path.join(PASTA, "ids_unicos_acidentes_2023.parquet")
ARQ_VITIMAS = os.path.join(PASTA, "vitimas_consolidado_2023.parquet")  # apenas leitura
ARQ_SAIDA = os.path.join(PASTA, "vitimas_consolidado_2023_filtrado.parquet")  # novo arquivo

BATCH_SIZE = 1_000_000

# 1. Carregar IDs únicos
print("📂 Carregando IDs únicos de acidentes...")
ids_unicos = set(
    pq.read_table(ARQ_IDS, columns=['num_acidente'])
    .column('num_acidente')
    .to_pylist()
)
print(f"   Total de IDs válidos: {len(ids_unicos):,}\n")

# 2. Filtrar e gravar diretamente no arquivo de SAÍDA
print("🔍 Filtrando vítimas – removendo apenas IDs órfãos...")

# Lê o arquivo original usando um bloco que garante o fechamento
parquet_file = pq.ParquetFile(ARQ_VITIMAS)
total_original = parquet_file.metadata.num_rows

writer = None
linhas_lidas = 0
linhas_escritas = 0

with tqdm(total=total_original, desc="Processando", unit=" linhas") as pbar:
    for batch in parquet_file.iter_batches(batch_size=BATCH_SIZE):
        table = pa.Table.from_batches([batch])

        mask = pc.is_in(
            table.column('num_acidente'),
            value_set=pa.array(list(ids_unicos), type=pa.int64())
        )
        filtrada = table.filter(mask)

        if writer is None and filtrada.num_rows > 0:
            writer = pq.ParquetWriter(ARQ_SAIDA, filtrada.schema, compression='snappy')

        if writer and filtrada.num_rows > 0:
            writer.write_table(filtrada)
            linhas_escritas += filtrada.num_rows

        linhas_lidas += table.num_rows
        pbar.update(table.num_rows)

# Fecha o leitor e o escritor
if writer:
    writer.close()
# Libera explicitamente o objeto ParquetFile (opcional, mas seguro)
del parquet_file

linhas_removidas = linhas_lidas - linhas_escritas

# 3. Feedback detalhado
print("\n" + "=" * 60)
print("RESULTADO DA FILTRAGEM")
print("=" * 60)
print(f"   Linhas originais : {linhas_lidas:,}")
print(f"   Linhas mantidas  : {linhas_escritas:,}")
print(f"   Linhas removidas : {linhas_removidas:,} ({linhas_removidas / linhas_lidas * 100:.2f}% do total)")
print(f"\n💾 Arquivo filtrado salvo em: {ARQ_SAIDA}")
print("   (O arquivo original 'vitimas_consolidado_2023.parquet' permanece inalterado.)")