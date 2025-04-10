import os
import json
from datetime import datetime

# Caminhos de arquivos com base na nova estrutura
json_path = "data/raw/dados_paises.json"  # Arquivo bruto de dados
log_path = "data/processed/LOG.txt"       # Log de execução
relatorio_path = "data/processed/RELATORIO_GERAL.txt"  # Relatório gerado

# Verifica se o JSON existe
if not os.path.exists(json_path):
    raise FileNotFoundError(f"Arquivo {json_path} não encontrado.")

# Carrega os dados
with open(json_path, "r", encoding="utf-8") as f:
    dados = json.load(f)

# Marca de tempo
agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Abre arquivos de saída
with open(log_path, "a", encoding="utf-8") as log, open(relatorio_path, "a", encoding="utf-8") as rel:
    log.write(f"[{agora}] GEOLOOP IA processou {len(dados)} países a partir de {json_path}\n")
    rel.write(f"\n=== RELATÓRIO GERAL (execução: {agora}) ===\n")

    for nome, pais in dados.items():
        capital = pais.get("capital", "Desconhecida")
        populacao = pais.get("populacao", "N/A")
        pib = pais.get("pib", "N/A")
        governo = pais.get("governo", "N/A")
        continente = pais.get("continente", "N/A")
        hdi = pais.get("hdi", "N/A")

        rel.write(f"\n📌 {nome} — Capital: {capital} | Continente: {continente}\n")
        rel.write(f"   População: {populacao} | PIB: {pib} | IDH: {hdi}\n")
        rel.write(f"   Governo: {governo}\n")
        rel.write(f"   ➤ Recomendações:\n")
        rel.write("     • Fortalecer relações diplomáticas regionais\n")
        rel.write("     • Investir em infraestrutura e IDH\n")
        rel.write("     • Promover estabilidade política\n")
