import os
import pyarrow.csv as csv
import pyarrow.parquet as pq

# Configuração
PASTA_RAW   = r"C:\Users\Programa\Desktop\DataFriend\RAW\Conjunto Extraído\2025"
PASTA_SAIDA = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2025"
os.makedirs(PASTA_SAIDA, exist_ok=True)

ARQUIVO_FONTE = os.path.join(PASTA_RAW, "12 - Acidentes_DadosAbertos.csv")
ARQUIVO_SAIDA = os.path.join(PASTA_SAIDA, "acidentes_consolidado_2025.parquet")

ENCODING  = 'latin1'
SEPARADOR = ';'

# Colunas que queremos manter (as mesmas de 2022, 2023 e 2024)
COLUNAS = [
    'num_acidente', 'ano_acidente', 'cond_meteorologica', 'data_acidente',
    'dia_semana', 'fase_dia', 'tp_acidente', 'uf_acidente', 'mes_acidente',
    'qtde_obitos', 'qtde_envolvidos', 'qtde_feridosilesos', 'chv_localidade'
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
print("✅ Arquivo de acidentes 2025 criado com sucesso.")