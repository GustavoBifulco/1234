#!/usr/bin/env python3
import requests
import json
import os
import time
import logging

# Configuração do logger para registrar as ações
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def fetch_country_data():
    """
    Busca dados dos países usando a API do Rest Countries.
    Tenta 3 vezes caso ocorra algum erro.
    """
    url = "https://restcountries.com/v3.1/all"
    for tentativa in range(3):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                logger.info("Sucesso na requisição da API")
                return response.json()
            else:
                logger.warning(f"Tentativa {tentativa+1}: Código {response.status_code}")
        except Exception as e:
            logger.error(f"Tentativa {tentativa+1} - Erro: {e}")
        time.sleep(3)
    raise Exception("Falha ao buscar dados após 3 tentativas")

def process_country_data(raw_data):
    """
    Processa os dados brutos; extrai nome, capital, população e continente.
    """
    processed_data = {}
    for country in raw_data:
        name = country.get("name", {}).get("common", "Desconhecido")
        capital = country.get("capital", ["Desconhecida"])
        population = country.get("population", "N/A")
        region = country.get("region", "N/A")
        processed_data[name] = {
            "capital": capital[0] if isinstance(capital, list) and capital else "Desconhecida",
            "populacao": population,
            "continente": region
        }
    return processed_data

def save_data(data, path="data/raw/dados_paises.json"):
    """
    Salva os dados processados em um arquivo JSON.
    Cria o diretório se necessário.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info(f"Dados salvos em {path}")

if __name__ == "__main__":
    try:
        logger.info("Iniciando processo de coleta de dados...")
        raw_data = fetch_country_data()
        logger.info("Processando os dados...")
        data = process_country_data(raw_data)
        logger.info("Salvando os dados processados...")
        save_data(data)
        logger.info("Data Ingest concluído com sucesso!")
    except Exception as e:
        logger.error("Erro ao executar data ingest: " + str(e))
