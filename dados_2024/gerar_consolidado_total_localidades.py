import os
import pyarrow.csv as csv
import pyarrow.parquet as pq

# Configuração
PASTA_RAW   = r"C:\Users\Programa\Desktop\DataFriend\RAW\Conjunto Extraído\2024"
PASTA_SAIDA = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2024"
os.makedirs(PASTA_SAIDA, exist_ok=True)

ARQUIVO_FONTE = os.path.join(PASTA_RAW, "12 - Localidade_DadosAbertos.csv")
ARQUIVO_SAIDA = os.path.join(PASTA_SAIDA, "localidades_consolidado_2024.parquet")

ENCODING  = 'latin1'
SEPARADOR = ';'

# Colunas que queremos manter (as mesmas de 2022 e 2023)
COLUNAS = [
    'chv_localidade', 'ano_referencia', 'regiao', 'uf', 'municipio',
    'regiao_metropolitana', 'qtde_habitantes', 'frota_total', 'frota_circulante'
]

print(f"📄 Lendo arquivo: {os.path.basename(ARQUIVO_FONTE)}")
read_options = csv.ReadOptions(encoding=ENCODING)
parse_options = csv.ParseOptions(delimiter=SEPARADOR)
convert_options = csv.ConvertOptions(include_columns=COLUNAS)

tabela = csv.read_csv(
    ARQUIVO_FONTE,
    read_options=read_options,
    parse_options=parse_options,
    convert_options=convert_options
)

print(f"   Linhas carregadas: {tabela.num_rows:,}")
print(f"   Colunas: {tabela.column_names}")

# Salva como Parquet
print(f"💾 Salvando em {ARQUIVO_SAIDA}...")
pq.write_table(tabela, ARQUIVO_SAIDA, compression='snappy')
print("✅ Arquivo de localidades 2024 criado com sucesso.")