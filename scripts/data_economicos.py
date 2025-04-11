#!/usr/bin/env python3
import requests
import json
import os
import logging

# Configuração do logger para debugar
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def fetch_economic_data(country_code="all", indicator="NY.GDP.MKTP.CD", start_year=2019, end_year=2020):
    """
    Busca dados econômicos (PIB) usando a API do Banco Mundial
    para TODOS os países (incluindo agregados). Depois, filtra para deixar
    somente os dados dos países individuais.
    """
    # O parâmetro per_page=5000 ajuda a retornar todos os registros em uma única página.
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json&date={start_year}:{end_year}&per_page=5000"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Resposta completa da API: {data}")
            if len(data) > 1 and data[1]:
                logger.info("Dados econômicos obtidos com sucesso.")
                # Lista de IDs de agregados (regiões) que queremos filtrar
                aggregate_ids = ["1A", "B8", "S3", "ZH", "ZI"]
                filtered = [item for item in data[1] if item["country"]["id"] not in aggregate_ids]
                logger.info(f"Registros após filtragem: {len(filtered)} (apenas países individuais)")
                return filtered
            else:
                logger.warning("Nenhum dado encontrado na resposta da API.")
        else:
            logger.error(f"Erro ao acessar a API: Código {response.status_code}")
    except Exception as e:
        logger.error(f"Erro na requisição: {e}")
    return None

def save_economic_data(data, path="data/raw/economic_data.json"):
    """
    Salva os dados econômicos em um arquivo JSON usando caminho absoluto.
    """
    if data:
        abs_path = os.path.abspath(path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"Dados econômicos salvos em {abs_path}")
    else:
        logger.warning("Dados vazios. Nenhum arquivo foi criado.")

if __name__ == "__main__":
    logger.info("Iniciando coleta de dados econômicos para todos os países...")
    economic_data = fetch_economic_data()
    save_economic_data(economic_data)
