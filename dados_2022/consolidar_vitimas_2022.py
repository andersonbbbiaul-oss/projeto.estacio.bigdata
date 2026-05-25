import os
import pyarrow.csv as csv
import pyarrow.parquet as pq

# Configuração
PASTA_RAW   = r"C:\Users\Programa\Desktop\DataFriend\RAW\Conjunto Extraído\2022"
PASTA_SAIDA = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2022"

ARQUIVO_FONTE = os.path.join(PASTA_RAW, "9 - Vitimas_DadosAbertos_Setembro.csv")
ARQUIVO_SAIDA = os.path.join(PASTA_SAIDA, "vitimas_consolidado_2022.parquet")

ENCODING  = 'latin1'
SEPARADOR = ';'

# Colunas que queremos manter
COLUNAS = ['num_acidente', 'faixa_idade', 'genero', 'tp_envolvido', 'ind_motorista']

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

# Salva como Parquet (sobrescreve o existente)
print(f"💾 Salvando em {ARQUIVO_SAIDA}...")
pq.write_table(tabela, ARQUIVO_SAIDA, compression='snappy')
print("✅ Novo arquivo de vítimas 2022 criado com sucesso.")