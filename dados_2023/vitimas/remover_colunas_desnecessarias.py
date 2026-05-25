import os
import pyarrow.csv as csv
import pyarrow.parquet as pq

PASTA_RAW   = r"C:\Users\Programa\Desktop\DataFriend\RAW\Conjunto Extraído\2023"
PASTA_SAIDA = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2023"
os.makedirs(PASTA_SAIDA, exist_ok=True)

ARQUIVO_FONTE = os.path.join(PASTA_RAW, "1 - Vitimas_DadosAbertos.csv")
ARQUIVO_SAIDA = os.path.join(PASTA_SAIDA, "vitimas_consolidado_2023.parquet")

ENCODING  = 'latin1'
SEPARADOR = ';'

COLUNAS = ['num_acidente', 'faixa_idade', 'genero', 'tp_envolvido', 'ind_motorista']

print("📄 Lendo arquivo de vítimas (apenas colunas selecionadas)...")
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

print(f"💾 Salvando em {ARQUIVO_SAIDA}...")
pq.write_table(tabela, ARQUIVO_SAIDA, compression='snappy')
print("✅ Arquivo de vítimas consolidado criado com sucesso.")