#!/usr/bin/env python3
import requests
import json
import os
import time
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def fetch_economic_data(country_code="BRA", indicator="NY.GDP.MKTP.CD", start_year=2019, end_year=2020):
    """
    Busca dados do PIB para um país usando a API do Banco Mundial.
    Exemplo: country_code="BRA" para Brasil; indicador é PIB (current US$)
    """
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json&date={start_year}:{end_year}"
    for attempt in range(3):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                logger.info("Sucesso ao buscar dados econômicos")
                data = response.json()
                # A API retorna uma lista; os dados úteis estão na segunda posição
                return data[1] if len(data) > 1 else None
            else:
                logger.warning(f"Tentativa {attempt+1}: Código {response.status_code}")
        except Exception as e:
            logger.error(f"Tentativa {attempt+1} - Erro: {e}")
        time.sleep(2)
    raise Exception("Falha ao buscar dados econômicos após 3 tentativas")

def save_economic_data(data, path="data/raw/economic_data.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info(f"Dados econômicos salvos em {path}")

if __name__ == "__main__":
    try:
        logger.info("Iniciando coleta de dados econômicos...")
        econ_data = fetch_economic_data()
        save_economic_data(econ_data)
        logger.info("Coleta de dados econômicos concluída!")
    except Exception as e:
        logger.error("Erro na coleta de dados econômicos: " + str(e))
