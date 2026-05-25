import os
import pyarrow.csv as csv
import pyarrow.parquet as pq

# Configurações
PASTA_RAW = r"C:\Users\Programa\Desktop\DataFriend\RAW\Conjunto Extraído\2023"
PASTA_SAIDA = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2023"
os.makedirs(PASTA_SAIDA, exist_ok=True)

ARQUIVO_FONTE = os.path.join(PASTA_RAW, "1 - Acidentes_DadosAbertos.csv")
ARQUIVO_SAIDA = os.path.join(PASTA_SAIDA, "acidentes_consolidado_2023.parquet")

ENCODING = 'latin1'
SEPARADOR = ';'

# Colunas que queremos manter
COLUNAS = [
    'num_acidente', 'ano_acidente', 'cond_meteorologica', 'data_acidente',
    'dia_semana', 'fase_dia', 'tp_acidente', 'uf_acidente', 'mes_acidente',
    'qtde_obitos', 'qtde_envolvidos', 'qtde_feridosilesos', 'chv_localidade'
]

print(f"📂 Lendo arquivo: {ARQUIVO_FONTE}")
read_options = csv.ReadOptions(encoding=ENCODING)
parse_options = csv.ParseOptions(delimiter=SEPARADOR)
convert_options = csv.ConvertOptions(include_columns=COLUNAS)

# Lê apenas as colunas desejadas
tabela = csv.read_csv(
    ARQUIVO_FONTE,
    read_options=read_options,
    parse_options=parse_options,
    convert_options=convert_options
)

print(f"   Registros carregados: {tabela.num_rows:,}")
print(f"   Colunas: {tabela.column_names}")

# Salva em Parquet
print(f"💾 Salvando em {ARQUIVO_SAIDA}...")
pq.write_table(tabela, ARQUIVO_SAIDA, compression='snappy')
print("✅ Arquivo consolidado de acidentes 2023 criado com sucesso.")