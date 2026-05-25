import os
import pyarrow.csv as csv
import pyarrow.parquet as pq

PASTA_2022 = r"C:\Users\Programa\Desktop\DataFriend\RAW\Conjunto Extraído\2022"
ARQ_ACIDENTES = os.path.join(PASTA_2022, "9 - Acidentes_DadosAbertos_Setembro.csv")
ARQ_VEICULOS  = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2022\veiculos_consolidado_2022.parquet"

# Carrega IDs de veículos (todos)
ids_ve = set(pq.read_table(ARQ_VEICULOS, columns=['num_acidente']).column('num_acidente').to_pylist())
# Carrega IDs de acidentes do CSV de setembro
read_options = csv.ReadOptions(encoding='latin1')
parse_options = csv.ParseOptions(delimiter=';')
convert_options = csv.ConvertOptions(include_columns=['num_acidente'])
tabela_ac = csv.read_csv(ARQ_ACIDENTES, read_options=read_options, parse_options=parse_options, convert_options=convert_options)
ids_ac_csv = set(tabela_ac.column('num_acidente').to_pylist())

orfãos = ids_ve - ids_ac_csv
print(f"IDs de veículos: {len(ids_ve):,}")
print(f"IDs no CSV de acidentes de setembro: {len(ids_ac_csv):,}")
print(f"IDs de veículos que NÃO estão no CSV de acidentes: {len(orfãos):,}")
if orfãos:
    print("Exemplos:", sorted(list(orfãos))[:10])