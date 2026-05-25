import os
import pyarrow.csv as csv
import pyarrow.parquet as pq
import pyarrow as pa
import pyarrow.compute as pc

# ----------------------------------------------------------
# Configuração
# ----------------------------------------------------------
PASTA_RAW   = r"C:\Users\Programa\Desktop\DataFriend\RAW\Conjunto Extraído\2023"
PASTA_SAIDA = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2023"
os.makedirs(PASTA_SAIDA, exist_ok=True)

ARQ_ACIDENTES   = os.path.join(PASTA_SAIDA, "acidentes_consolidado_2023.parquet")
ARQ_LOC_ORIG    = os.path.join(PASTA_RAW, "1 - Localidade_DadosAbertos.csv")
ARQ_LOC_SAIDA   = os.path.join(PASTA_SAIDA, "localidades_consolidado_2023.parquet")

ENCODING  = 'latin1'
SEPARADOR = ';'

# Colunas que queremos manter na tabela final de localidades
COLUNAS_LOC = [
    'chv_localidade', 'ano_referencia', 'regiao', 'uf', 'municipio',
    'regiao_metropolitana', 'qtde_habitantes', 'frota_total', 'frota_circulante'
]

# ----------------------------------------------------------
# 1. Obter o conjunto de chv_localidade usadas nos acidentes
# ----------------------------------------------------------
print("📂 Obtendo chaves de localidade dos acidentes...")
tabela_ac = pq.read_table(ARQ_ACIDENTES, columns=['chv_localidade'])
chaves_unicas = set(tabela_ac.column('chv_localidade').to_pylist())
print(f"   Chaves distintas nos acidentes: {len(chaves_unicas):,}")

# ----------------------------------------------------------
# 2. Ler o CSV original de localidades e filtrar
# ----------------------------------------------------------
print(f"📄 Lendo localidades originais: {os.path.basename(ARQ_LOC_ORIG)}")
read_options    = csv.ReadOptions(encoding=ENCODING)
parse_options   = csv.ParseOptions(delimiter=SEPARADOR)
convert_options = csv.ConvertOptions(include_columns=COLUNAS_LOC)

tabela_loc = csv.read_csv(
    ARQ_LOC_ORIG,
    read_options=read_options,
    parse_options=parse_options,
    convert_options=convert_options
)

# Filtra apenas as linhas cuja chv_localidade está no conjunto dos acidentes
mask = pc.is_in(tabela_loc.column('chv_localidade'), value_set=pa.array(list(chaves_unicas), type=pa.string()))
tabela_filtrada = tabela_loc.filter(mask)
df_loc = tabela_filtrada.to_pandas()
print(f"   Localidades antes: {tabela_loc.num_rows:,}")
print(f"   Localidades após filtro: {len(df_loc):,}")

# ----------------------------------------------------------
# 3. Remover duplicatas – uma linha por combinação chv_localidade + ano
# ----------------------------------------------------------
df_unique = df_loc.drop_duplicates(subset=['chv_localidade', 'ano_referencia'])
print(f"   Combinações únicas (localidade + ano): {len(df_unique):,}")

# ----------------------------------------------------------
# 4. Salvar o novo Parquet (sem a coluna num_acidente)
# ----------------------------------------------------------
print(f"💾 Salvando em {ARQ_LOC_SAIDA}...")
df_unique.to_parquet(ARQ_LOC_SAIDA, index=False)
print("✅ Arquivo de localidades consolidado (apenas combinações únicas localidade+ano) criado.")