import os
import pyarrow.parquet as pq
import pyarrow.compute as pc
import pandas as pd
import numpy as np

# ------------------------------------------------------------
# Configuração
# ------------------------------------------------------------
PASTA = r"C:\Users\Programa\Desktop\DataFriend\TRABALHO_2025"

ARQ_ACIDENTES   = os.path.join(PASTA, "acidentes_consolidado_2025.parquet")
ARQ_LOCALIDADES = os.path.join(PASTA, "localidades_consolidado_filtrado_2025.parquet")  # arquivo enxuto, sem num_acidente
ARQ_VEICULOS    = os.path.join(PASTA, "veiculos_consolidado_2025.parquet")
ARQ_VITIMAS     = os.path.join(PASTA, "vitimas_consolidado_2025.parquet")

# ------------------------------------------------------------
# Funções auxiliares
# ------------------------------------------------------------
resultados = []

def check(condicao, msg_ok, msg_falha):
    if condicao:
        resultados.append(f"✅ {msg_ok}")
    else:
        resultados.append(f"❌ {msg_falha}")

# ------------------------------------------------------------
# ETAPA 0 – Validação das colunas esperadas
# ------------------------------------------------------------
COLUNAS_ACIDENTES   = ['num_acidente', 'ano_acidente', 'mes_acidente', 'data_acidente',
                       'uf_acidente', 'tp_acidente', 'fase_dia', 'dia_semana',
                       'cond_meteorologica', 'qtde_obitos', 'qtde_envolvidos',
                       'qtde_feridosilesos', 'chv_localidade']
COLUNAS_LOCALIDADES = ['chv_localidade', 'ano_referencia', 'regiao', 'uf', 'municipio',
                       'regiao_metropolitana', 'qtde_habitantes', 'frota_total', 'frota_circulante']
COLUNAS_VEICULOS    = ['num_acidente', 'tipo_veiculo', 'qtde_veiculos']
COLUNAS_VITIMAS     = ['num_acidente', 'faixa_idade', 'genero', 'tp_envolvido', 'ind_motorista']

print("=" * 70)
print("ETAPA 0 – VALIDAÇÃO DAS COLUNAS ESPERADAS")
print("=" * 70)

def validar_colunas(arquivo, nome, colunas_esperadas):
    if not os.path.exists(arquivo):
        check(False, "", f"{nome}: arquivo não encontrado")
        return False
    schema = pq.read_schema(arquivo)
    presentes = set(schema.names)
    esperadas = set(colunas_esperadas)
    faltam = esperadas - presentes
    extras = presentes - esperadas
    if faltam:
        check(False, "", f"{nome}: colunas FALTANDO → {sorted(faltam)}")
    if extras:
        check(False, "", f"{nome}: colunas EXTRAS → {sorted(extras)}")
    if not faltam and not extras:
        check(True, f"{nome}: todas as colunas esperadas presentes", "")
        return True
    return False

ok1 = validar_colunas(ARQ_ACIDENTES,   "Acidentes",   COLUNAS_ACIDENTES)
ok2 = validar_colunas(ARQ_LOCALIDADES, "Localidades", COLUNAS_LOCALIDADES)
ok3 = validar_colunas(ARQ_VEICULOS,    "Veículos",    COLUNAS_VEICULOS)
ok4 = validar_colunas(ARQ_VITIMAS,     "Vítimas",     COLUNAS_VITIMAS)

if not all([ok1, ok2, ok3, ok4]):
    print("\n❌ Diferenças nas colunas encontradas. O script foi interrompido para evitar erros.")
    exit(1)

# ------------------------------------------------------------
# 1. Metadados e contagens
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("VERIFICAÇÃO COMPLETA – CONSOLIDADOS 2025 (29 itens)")
print("=" * 70)

meta_ac = pq.read_metadata(ARQ_ACIDENTES)
meta_lo = pq.read_metadata(ARQ_LOCALIDADES)
meta_ve = pq.read_metadata(ARQ_VEICULOS)
meta_vi = pq.read_metadata(ARQ_VITIMAS)

n_ac = meta_ac.num_rows
n_lo = meta_lo.num_rows
n_ve = meta_ve.num_rows
n_vi = meta_vi.num_rows

print(f"\n📏 Linhas: Acidentes={n_ac:,}  Localidades={n_lo:,}  Veículos={n_ve:,}  Vítimas={n_vi:,}")

# ------------------------------------------------------------
# 2. Carregamento de chaves (PyArrow, apenas colunas necessárias)
# ------------------------------------------------------------
print("\n📂 Carregando chaves para verificações...")
ids_ac = set(pq.read_table(ARQ_ACIDENTES, columns=['num_acidente']).column('num_acidente').to_pylist())
ids_ve = set(pq.read_table(ARQ_VEICULOS, columns=['num_acidente']).column('num_acidente').to_pylist())
ids_vi = set(pq.read_table(ARQ_VITIMAS, columns=['num_acidente']).column('num_acidente').to_pylist())

# Para localidades: chv_localidade e ano_referencia (sem num_acidente)
tab_lo = pq.read_table(ARQ_LOCALIDADES, columns=['chv_localidade', 'ano_referencia'])
chv_lo = set(tab_lo.column('chv_localidade').to_pylist())
pares_lo = set(zip(tab_lo.column('chv_localidade').to_pylist(),
                   tab_lo.column('ano_referencia').to_pylist()))

# Acidentes: chv_localidade e ano_acidente
tab_ac = pq.read_table(ARQ_ACIDENTES, columns=['chv_localidade', 'ano_acidente'])
chv_ac = set(tab_ac.column('chv_localidade').to_pylist())
pares_ac = set(zip(tab_ac.column('chv_localidade').to_pylist(),
                   tab_ac.column('ano_acidente').to_pylist()))

# ------------------------------------------------------------
# 3. DataFrames para verificações específicas (apenas colunas necessárias)
# ------------------------------------------------------------
df_ac = pd.read_parquet(ARQ_ACIDENTES, columns=[
    'num_acidente', 'ano_acidente', 'mes_acidente', 'data_acidente',
    'uf_acidente', 'tp_acidente', 'fase_dia', 'dia_semana', 'cond_meteorologica',
    'qtde_obitos', 'qtde_envolvidos', 'qtde_feridosilesos'
])
df_ve = pd.read_parquet(ARQ_VEICULOS, columns=['num_acidente', 'tipo_veiculo'])
df_vi = pd.read_parquet(ARQ_VITIMAS)
df_lo = pd.read_parquet(ARQ_LOCALIDADES, columns=[
    'chv_localidade', 'ano_referencia', 'uf', 'municipio', 'regiao',
    'qtde_habitantes', 'frota_total', 'frota_circulante', 'regiao_metropolitana'
])

# ============================================================
# VERIFICAÇÕES (29 itens)
# ============================================================

# --- 1. Integridade referencial (4 itens) ---
print("\n🔗 Integridade referencial...")
check(ids_ve.issubset(ids_ac),
      "Veículos → Acidentes (num_acidente) OK",
      f"Existem {len(ids_ve - ids_ac)} IDs em Veículos que não estão em Acidentes")
check(ids_vi.issubset(ids_ac),
      "Vítimas → Acidentes (num_acidente) OK",
      f"Existem {len(ids_vi - ids_ac)} IDs em Vítimas que não estão em Acidentes")
check(chv_ac.issubset(chv_lo),
      "Acidentes → Localidades (chv_localidade) OK",
      f"Existem {len(chv_ac - chv_lo)} chaves em Acidentes que não estão em Localidades")
check(pares_ac.issubset(pares_lo),
      "Acidentes → Localidades (chv+ano) OK",
      f"Existem {len(pares_ac - pares_lo)} combinações chv+ano em Acidentes que não estão em Localidades")

# --- 2. Unicidade de chaves (4 itens) ---
print("\n🔑 Unicidade...")
check(df_ac['num_acidente'].is_unique,
      "num_acidente único em Acidentes",
      "num_acidente duplicado em Acidentes")
dup_ve = df_ve.duplicated(subset=['num_acidente', 'tipo_veiculo']).sum()
check(dup_ve == 0,
      "Par (num_acidente, tipo_veiculo) único em Veículos",
      f"{dup_ve} duplicatas em Veículos")
dup_lo = df_lo.duplicated(subset=['chv_localidade', 'ano_referencia']).sum()
check(dup_lo == 0,
      "Par (chv_localidade, ano_referencia) único em Localidades",
      f"{dup_lo} duplicatas em Localidades")
dup_vi = df_vi.duplicated().sum()
check(dup_vi == 0,
      "Vítimas sem duplicatas exatas",
      f"Vítimas: {dup_vi} linhas duplicadas exatas (alertando, sem remover)")

# --- 3. Nulos (4 tabelas) ---
print("\n🚫 Nulos...")
def verificar_nulos(df, nome):
    nulos = df.isnull().sum()
    nulos_pos = nulos[nulos > 0]
    if len(nulos_pos) == 0:
        check(True, f"Sem nulos em {nome}", "")
    else:
        for col, qtd in nulos_pos.items():
            check(False, "", f"{nome}: coluna '{col}' com {qtd} nulos")

verificar_nulos(df_ac, "Acidentes")
verificar_nulos(df_lo, "Localidades")
verificar_nulos(df_ve, "Veículos")
verificar_nulos(df_vi, "Vítimas")

# --- 4. Consistência numérica (3 itens) ---
print("\n🔢 Consistência numérica...")
soma_envolvidos = df_ac['qtde_envolvidos'].sum()
soma_vitimas = n_vi
diff = abs(soma_envolvidos - soma_vitimas)
perc_diff = diff / soma_envolvidos * 100
check(perc_diff < 1.0,
      f"Soma qtde_envolvidos ({soma_envolvidos:,}) vs total vítimas ({soma_vitimas:,}) – diferença {perc_diff:.2f}% (<1%)",
      f"Diferença entre envolvidos e vítimas é {perc_diff:.2f}% (>1%)")
mask_corr = df_ac['qtde_envolvidos'] >= (df_ac['qtde_feridosilesos'] + df_ac['qtde_obitos'])
check(mask_corr.all(),
      "qtde_envolvidos >= feridos+obitos em todos os registros",
      f"{(~mask_corr).sum()} registros violam a condição")
negativos = (df_ac[['qtde_obitos', 'qtde_envolvidos', 'qtde_feridosilesos']] < 0).any(axis=1).sum()
check(negativos == 0,
      "Nenhum valor negativo em colunas numéricas",
      f"{negativos} linhas com valores negativos")

# --- 5. Consistência temporal (3 itens) ---
print("\n📅 Consistência temporal...")
# Ajuste: 2025 contém até 2025
anos_validos = set(range(2018, 2026))
anos_presentes = set(df_ac['ano_acidente'].unique())
check(anos_presentes == anos_validos,
      "Anos de 2018 a 2025 presentes",
      f"Anos encontrados: {sorted(anos_presentes)} (esperado {sorted(anos_validos)})")
meses_presentes = set(df_ac['mes_acidente'].unique())
check(meses_presentes == set(range(1,13)),
      "Meses de 1 a 12 presentes",
      f"Meses encontrados: {sorted(meses_presentes)}")
df_ac['data_dt'] = pd.to_datetime(df_ac['data_acidente'])
mes_da_data = df_ac['data_dt'].dt.month
check((mes_da_data == df_ac['mes_acidente']).all(),
      "Mês extraído da data coincide com mes_acidente",
      "Existem divergências entre data e mes_acidente")

# --- 6. Domínios de categorias (6 itens) ---
print("\n🏷️ Domínios...")
check(df_ac['uf_acidente'].nunique() == 27,
      "27 UFs em Acidentes",
      f"{df_ac['uf_acidente'].nunique()} UFs em Acidentes")
check(df_lo['uf'].nunique() == 27,
      "27 UFs em Localidades",
      f"{df_lo['uf'].nunique()} UFs em Localidades")
check(df_ac['tp_acidente'].nunique() == 16,
      "16 tipos de acidente",
      f"{df_ac['tp_acidente'].nunique()} tipos")
check(df_ac['dia_semana'].nunique() == 7,
      "7 dias da semana",
      f"{df_ac['dia_semana'].nunique()} dias")
check(df_ac['fase_dia'].nunique() == 6,
      "6 fases do dia",
      f"{df_ac['fase_dia'].nunique()} fases")
check(df_ac['cond_meteorologica'].nunique() == 11,
      "11 condições meteorológicas",
      f"{df_ac['cond_meteorologica'].nunique()} condições")

# --- 7. Cobertura entre tabelas (3 itens) ---
print("\n📊 Cobertura...")
sem_veic = len(ids_ac - ids_ve)
check(sem_veic == 0,
      f"Acidentes sem veículos: {sem_veic} (0.00%)",
      f"Acidentes sem veículos: {sem_veic}")
sem_vit = len(ids_ac - ids_vi)
check(sem_vit == 0,
      "Todos os acidentes têm vítimas",
      f"Acidentes sem vítimas: {sem_vit}")
check(chv_ac.issubset(chv_lo),
      "Todos os acidentes possuem localidade (chv_localidade presente em Localidades)",
      f"Existem {len(chv_ac - chv_lo)} chaves de acidentes sem localidade")

# --- 8. Distribuições rápidas (5 itens) ---
print("\n📈 Distribuições...")
ac_por_ano = df_ac.groupby('ano_acidente').size()
obitos_por_ano = df_ac.groupby('ano_acidente')['qtde_obitos'].sum()
envolvidos_por_ano = df_ac.groupby('ano_acidente')['qtde_envolvidos'].sum()
feridos_por_ano = df_ac.groupby('ano_acidente')['qtde_feridosilesos'].sum()
print("   Totais por ano:")
for ano in sorted(ac_por_ano.index):
    print(f"   {ano}: Acidentes={ac_por_ano[ano]:,}  Óbitos={obitos_por_ano[ano]:,}  Envolvidos={envolvidos_por_ano[ano]:,}  Feridos={feridos_por_ano[ano]:,}")

top5_uf = df_ac['uf_acidente'].value_counts().head(5)
print("\n   Top 5 UFs com mais acidentes:")
for uf, qtd in top5_uf.items():
    print(f"   {uf}: {qtd:,}")

media_veic = n_ve / n_ac
media_vit = n_vi / n_ac
print(f"\n   Média de veículos por acidente: {media_veic:.2f}")
print(f"   Média de vítimas por acidente: {media_vit:.2f}")

# --- 9. Metadados e tamanhos (4 itens) ---
print("\n📁 Estrutura e tamanhos...")
for nome, arq in [("Acidentes", ARQ_ACIDENTES), ("Localidades", ARQ_LOCALIDADES),
                  ("Veículos", ARQ_VEICULOS), ("Vítimas", ARQ_VITIMAS)]:
    size_mb = os.path.getsize(arq) / (1024**2)
    print(f"   {nome}: {size_mb:.2f} MB")

# ------------------------------------------------------------
# Relatório final
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("RESULTADO DAS 29 VERIFICAÇÕES")
print("=" * 70)
for linha in resultados:
    print(linha)
print("\n✅ Verificação concluída.")