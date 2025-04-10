import os
import json
import random
from datetime import datetime

# Caminhos dos arquivos conforme a estrutura do repositório
json_path = "data/raw/dados_paises.json"          # Fonte bruta dos dados de países
log_path = "data/processed/LOG.txt"                # Arquivo de log de execução
relatorio_path = "data/processed/RELATORIO_GERAL.txt"  # Relatório de simulação gerado

# Verifica se o arquivo JSON existe na pasta correta
if not os.path.exists(json_path):
    raise FileNotFoundError(f"Arquivo {json_path} não encontrado.")

# Carrega os dados dos países
with open(json_path, "r", encoding="utf-8") as f:
    dados = json.load(f)

# Marca de tempo para o log e relatório
agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Abre os arquivos de saída (logs e relatório de simulação)
with open(log_path, "a", encoding="utf-8") as log, open(relatorio_path, "a", encoding="utf-8") as rel:
    log.write(f"[{agora}] GEOLOOP AI processou {len(dados)} países a partir de {json_path}\n")
    rel.write(f"\n=== RELATÓRIO GERAL DE SIMULAÇÃO (execução: {agora}) ===\n")

    # Para cada país nos dados, realiza simulações e recomendações internas ao jogo
    for nome, pais in dados.items():
        # Extraindo informações básicas
        capital = pais.get("capital", "Desconhecida")
        populacao = pais.get("populacao", "N/A")
        pib = pais.get("pib", "N/A")
        governo = pais.get("governo", "N/A")
        continente = pais.get("continente", "N/A")
        hdi = pais.get("hdi", "N/A")
        
        # Simulação de elementos internos do jogo com base nos dados:
        # 1. Definir estratégias econômicas e vínculo institucional por meio do PIB
        if pib != "N/A" and isinstance(pib, (int, float)):
            if pib > 1e6:
                economia_status = "alta produção, tecnologia avançada e investimentos robustos"
                ministerio_economia = "Ministério da Inovação Econômica"
            else:
                economia_status = "desenvolvimento focado no suporte social e crescimento gradual"
                ministerio_economia = "Ministério da Economia e Desenvolvimento Social"
        else:
            economia_status = "dados insuficientes para avaliação econômica"
            ministerio_economia = "Ministério Genérico da Economia"
        
        # 2. Determinar o grau de influência internacional baseado no IDH
        if hdi != "N/A" and isinstance(hdi, (float, int)):
            if hdi >= 0.8:
                influencia = "alta"
            elif hdi >= 0.5:
                influencia = "moderada"
            else:
                influencia = "baixa"
        else:
            influencia = "não definida"
        
        # 3. Simular eventos estratégicos ou crises internas para enriquecer a mecânica do jogo
        eventos = [
            "Nenhum evento crítico",
            "Crise diplomática emergente",
            "Formação de nova aliança estratégica",
            "Aumento da tensão militar",
            "Intervenção humanitária inesperada"
        ]
        evento_selecionado = random.choice(eventos)
        
        # 4. Gerar recomendações e ações de simulação para o jogo
        rel.write(f"\n📌 {nome} — Capital: {capital} | Continente: {continente}\n")
        rel.write(f"   População: {populacao} | PIB: {pib} | IDH: {hdi}\n")
        rel.write(f"   Governo: {governo}\n")
        rel.write(f"   ➤ Recomendações de Simulação:\n")
        rel.write(f"     • Proposta: Reestruturar o setor econômico com a criação do {ministerio_economia}.\n")
        rel.write(f"       - Justificativa: {economia_status}.\n")
        rel.write(f"     • Sistema de influência internacional definido como {influencia}.\n")
        rel.write(f"     • Evento dinâmico simulado: {evento_selecionado}\n")
        rel.write("     • Avaliar atualização de ministérios e medidas políticas com base nas operações do cenário global.\n")
        
        # Aqui, você pode expandir a lógica para autoavaliar e ajustar outras estruturas,
        # como dados diplomáticos, sistemas de defesa e eventos socioeconômicos.
