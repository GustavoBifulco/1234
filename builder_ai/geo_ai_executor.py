import os
import json
from datetime import datetime
from pathlib import Path

# Caminho da pasta de países
pasta_paises = Path("countries")
pasta_paises.mkdir(parents=True, exist_ok=True)

# Lista de países da ONU simplificada (exemplo com 10, pode expandir para 193)
paises = [
    {"nome": "Brasil", "regime": "Presidencialismo", "presidente": "Luiz Inácio Lula da Silva", "pib": "2.1 tri USD", "idh": 0.765, "populacao": "215 milhões"},
    {"nome": "Estados Unidos", "regime": "Presidencialismo", "presidente": "Joe Biden", "pib": "25 tri USD", "idh": 0.921, "populacao": "332 milhões"},
    {"nome": "China", "regime": "Partido Único", "presidente": "Xi Jinping", "pib": "17.7 tri USD", "idh": 0.768, "populacao": "1.4 bilhões"},
    {"nome": "Rússia", "regime": "Presidencialismo Autoritário", "presidente": "Vladimir Putin", "pib": "1.7 tri USD", "idh": 0.822, "populacao": "144 milhões"},
    {"nome": "Índia", "regime": "Parlamentarismo", "presidente": "Droupadi Murmu", "pib": "3.7 tri USD", "idh": 0.633, "populacao": "1.42 bilhões"},
    {"nome": "França", "regime": "Semipresidencialismo", "presidente": "Emmanuel Macron", "pib": "3.2 tri USD", "idh": 0.903, "populacao": "67 milhões"},
    {"nome": "Japão", "regime": "Monarquia Parlamentarista", "presidente": "Fumio Kishida", "pib": "4.9 tri USD", "idh": 0.925, "populacao": "125 milhões"},
    {"nome": "Alemanha", "regime": "Parlamentarismo", "presidente": "Frank-Walter Steinmeier", "pib": "4.2 tri USD", "idh": 0.942, "populacao": "83 milhões"},
    {"nome": "Nigéria", "regime": "República Federal", "presidente": "Bola Ahmed Tinubu", "pib": "0.5 tri USD", "idh": 0.539, "populacao": "213 milhões"},
    {"nome": "Canadá", "regime": "Monarquia Parlamentarista", "presidente": "Justin Trudeau", "pib": "2.2 tri USD", "idh": 0.929, "populacao": "38 milhões"}
]

# Gerar arquivos JSON
for pais in paises:
    nome_arquivo = pais["nome"].lower().replace(" ", "_") + ".json"
    caminho = pasta_paises / nome_arquivo

    dados = {
        "nome": pais["nome"],
        "data_ultima_atualizacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "governo": {
            "sistema": pais["regime"],
            "presidente": pais["presidente"],
            "partidos": [],
            "proxima_eleicao": "Desconhecida"
        },
        "ministerios": [
            "Ministério da Defesa", "Ministério da Economia",
            "Ministério da Saúde", "Ministério da Educação"
        ],
        "leis_em_vigor": [
            "Lei de Orçamento Anual", "Lei de Segurança Nacional"
        ],
        "resumo_estrategico": f"{pais['nome']} deve revisar suas estratégias regionais e econômicas.",
        "indicadores": {
            "PIB": pais["pib"],
            "populacao": pais["populacao"],
            "IDH": pais["idh"]
        },
        "acoes_sugeridas": [
            "Fortalecer relações internacionais",
            "Reduzir desigualdade interna",
            "Aumentar investimentos em infraestrutura"
        ],
        "influencia_global": {
            "reputacao": 50,
            "aliados": [],
            "riscos": []
        }
    }

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

print("Arquivos de países gerados com sucesso.")