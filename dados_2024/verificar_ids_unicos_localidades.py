import os
import pyarrow.csv as csv

# Configuração
PASTA_2024 = r"C:\Users\Programa\Desktop\DataFriend\RAW\Conjunto Extraído\2024"
ENCODING   = 'latin1'
SEPARADOR  = ';'

# --- 1. Listar todos os arquivos de localidade e seus prefixos numéricos ---
print("📂 Procurando arquivos de Localidade em 2024...")
arquivos_mes = []
for arq in os.listdir(PASTA_2024):
    if not arq.endswith('.csv'):
        continue
    partes = arq.split(" - ", 1)
    if len(partes) == 2 and partes[1].startswith("Localidade"):
        try:
            mes = int(partes[0].strip())
            caminho = os.path.join(PASTA_2024, arq)
            arquivos_mes.append((mes, arq, caminho))
        except ValueError:
            pass

if not arquivos_mes:
    print("❌ Nenhum arquivo de Localidade encontrado.")
    exit()

arquivos_mes.sort(key=lambda x: x[0])
print(f"📋 Arquivos encontrados: {len(arquivos_mes)}")
for mes, nome, _ in arquivos_mes:
    print(f"   Mês {mes:2d} → {nome}")

# --- 2. Análise progressiva (do mês mais recente para o mais antigo) ---
print("\n🔍 Análise progressiva das chaves de localidade (do arquivo mais recente para o mais antigo):")
chaves_acumuladas = set()
for mes, nome, caminho in reversed(arquivos_mes):
    print(f"\n📄 Mês {mes:2d} – {nome}")
    read_options = csv.ReadOptions(encoding=ENCODING)
    parse_options = csv.ParseOptions(delimiter=SEPARADOR)
    convert_options = csv.ConvertOptions(include_columns=['chv_localidade'])
    tabela = csv.read_csv(
        caminho,
        read_options=read_options,
        parse_options=parse_options,
        convert_options=convert_options
    )
    chaves_arquivo = set(tabela.column('chv_localidade').to_pylist())
    novas = chaves_arquivo - chaves_acumuladas
    comuns = len(chaves_arquivo & chaves_acumuladas)
    print(f"   Total de chaves no arquivo: {len(chaves_arquivo):,}")
    print(f"   Chaves já conhecidas: {comuns:,}")
    print(f"   Chaves NOVAS (ainda não vistas): {len(novas):,}")
    if novas:
        print(f"   Exemplos de novas chaves: {sorted(list(novas))[:10]}")
    else:
        print("   Nenhuma chave nova – esse arquivo é totalmente coberto pelos mais recentes.")
    chaves_acumuladas.update(novas)

print(f"\n✅ Total de chaves únicas acumuladas após todos os arquivos: {len(chaves_acumuladas):,}")