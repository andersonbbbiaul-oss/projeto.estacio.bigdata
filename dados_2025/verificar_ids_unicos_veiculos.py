import os
import pyarrow.csv as csv

# Configuração
PASTA_2025 = r"C:\Users\Programa\Desktop\DataFriend\RAW\Conjunto Extraído\2025"
ENCODING   = 'latin1'
SEPARADOR  = ';'

# --- 1. Listar todos os arquivos de veículos e seus prefixos numéricos ---
print("📂 Procurando arquivos de TipoVeiculo em 2025...")
arquivos_mes = []
for arq in os.listdir(PASTA_2025):
    if not arq.endswith('.csv'):
        continue
    partes = arq.split(" - ", 1)
    if len(partes) == 2 and partes[1].startswith("TipoVeiculo"):
        try:
            mes = int(partes[0].strip())
            caminho = os.path.join(PASTA_2025, arq)
            arquivos_mes.append((mes, arq, caminho))
        except ValueError:
            pass

if not arquivos_mes:
    print("❌ Nenhum arquivo de TipoVeiculo encontrado.")
    exit()

arquivos_mes.sort(key=lambda x: x[0])
print(f"📋 Arquivos encontrados: {len(arquivos_mes)}")
for mes, nome, _ in arquivos_mes:
    print(f"   Mês {mes:2d} → {nome}")

# --- 2. Análise progressiva (do mês mais recente para o mais antigo) ---
print("\n🔍 Análise progressiva dos IDs (do arquivo mais recente para o mais antigo):")
ids_acumulados = set()

for mes, nome, caminho in reversed(arquivos_mes):
    print(f"\n📄 Mês {mes:2d} – {nome}")
    read_options = csv.ReadOptions(encoding=ENCODING)
    parse_options = csv.ParseOptions(delimiter=SEPARADOR)
    convert_options = csv.ConvertOptions(include_columns=['num_acidente'])
    tabela = csv.read_csv(
        caminho,
        read_options=read_options,
        parse_options=parse_options,
        convert_options=convert_options
    )
    ids_arquivo = set(tabela.column('num_acidente').to_pylist())
    novos = ids_arquivo - ids_acumulados
    comuns = len(ids_arquivo & ids_acumulados)
    print(f"   Total de IDs no arquivo: {len(ids_arquivo):,}")
    print(f"   IDs já conhecidos: {comuns:,}")
    print(f"   IDs NOVOS (ainda não vistos): {len(novos):,}")
    if novos:
        print(f"   Exemplos de novos IDs: {sorted(list(novos))[:10]}")
    else:
        print("   Nenhum ID novo – esse arquivo é totalmente coberto pelos mais recentes.")
    ids_acumulados.update(novos)

print(f"\n✅ Total de IDs únicos acumulados após todos os arquivos: {len(ids_acumulados):,}")