#!/usr/bin/env python3
import requests
import json
import os

def fetch_country_data():
    """
    Busca dados de países usando a API do Rest Countries.
    """
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Erro ao buscar dados dos países da API.")
    return response.json()

def process_country_data(raw_data):
    """
    Processa os dados brutos para manter apenas os campos desejados:
      - Nome do país
      - Capital (primeira, se existir)
      - População
      - Região (continente)
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
    Salva os dados processados no arquivo JSON.
    Cria o diretório, se necessário.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Dados salvos em", path)

if __name__ == "__main__":
    try:
        print("Buscando dados dos países...")
        raw_data = fetch_country_data()
        print("Processando dados...")
        data = process_country_data(raw_data)
        print("Salvando dados processados...")
        save_data(data)
        print("Data Ingest concluído com sucesso!")
    except Exception as e:
        print("Erro ao executar data ingest:", e)
