import os
import json
from datetime import datetime

# Caminhos
json_path = "dados_paises.json"
log_path = "LOG.txt"
relatorio_path = "RELATORIO_GERAL.txt"

# Validar existência
if not os.path.exists(json_path):
    raise FileNotFoundError("dados_paises.json não encontrado.")

# Carregar dados
with open(json_path, "r", encoding="utf-8") as f:
    dados_paises = json.load(f)

data_execucao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Gerar LOG e RELATÓRIO
with open(log_path, "a", encoding="utf-8") as log, open(relatorio_path, "a", encoding="utf-8") as rel:
    log.write(f"[{data_execucao}] IA analisou dados de {len(dados_paises)} países a partir do JSON único.\n")
    rel.write(f"\n=== RELATÓRIO GERAL - EXECUÇÃO {data_execucao} ===\n")

    for nome, dados in dados_paises.items():
        capital = dados.get("capital", "Desconhecida")
        sistema = dados.get("governo", "Desconhecido")
        populacao = dados.get("populacao", "N/A")
        hdi = dados.get("hdi", "N/A")
        continente = dados.get("continente", "Desconhecido")
        area = dados.get("area", "Desconhecida")

        rel.write(f"\n📌 País: {nome} | Capital: {capital} | Continente: {continente} | Área: {area}\n")
        rel.write(f"- Sistema de Governo: {sistema}\n")
        rel.write(f"- População estimada: {populacao}\n")
        rel.write(f"- IDH: {hdi}\n")
        rel.write(f"- Ações Sugeridas:\n")
        rel.write("  • Fortalecer educação básica\n")
        rel.write("  • Ampliar infraestrutura nacional\n")
        rel.write("  • Reforçar laços diplomáticos regionais\n")

print("Relatórios gerados com sucesso.")
