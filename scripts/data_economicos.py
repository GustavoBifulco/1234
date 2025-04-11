#!/usr/bin/env python3
import requests
import json
import os
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def fetch_economic_data(country_code="BRA", indicator="NY.GDP.MKTP.CD", start_year=2019, end_year=2020):
    """
    Busca dados econômicos (PIB) usando a API do Banco Mundial.
    """
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json&date={start_year}:{end_year}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logger.info("Sucesso ao acessar a API do Banco Mundial.")
            data = response.json()
            if len(data) > 1 and data[1]:  # Verifica se há dados no índice [1]
                return data[1]
            else:
                logger.warning("Nenhum dado encontrado na resposta da API.")
                return None
        else:
            logger.error(f"Erro ao acessar a API. Código de status: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Erro na requisição: {e}")
        return None

def save_economic_data(data, path="data/raw/economic_data.json"):
    """
    Salva os dados econômicos em um arquivo JSON.
    """
    if data:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"Dados econômicos salvos com sucesso em {path}")
    else:
        logger.warning("Os dados estavam vazios, então o arquivo não foi criado.")

if __name__ == "__main__":
    try:
        logger.info("Iniciando coleta de dados econômicos...")
        economic_data = fetch_economic_data()
        if economic_data:
            save_economic_data(economic_data)
        else:
            logger.warning("Nenhum dado econômico foi encontrado para salvar.")
    except Exception as e:
        logger.error(f"Erro na execução do script: {e}")
