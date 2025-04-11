#!/usr/bin/env python3
import requests
import json
import os
import time
import logging

# Leitura do arquivo de configuração dos indicadores
try:
    with open("config/indicators.json", "r", encoding="utf-8") as config_file:
        indicators_config = json.load(config_file)
    print("Configuração dos indicadores carregada com sucesso!")
except Exception as e:
    print("Erro ao ler o arquivo de configuração:", e)
    indicators_config = None

# Configuração do logger para registrar as ações
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Mapeamento de APIs para cada indicador
api_map = {
    "tipo_regime": "https://api.example.com/regime",
    "pib_nominal": "https://api.worldbank.org/v2/indicator/NY.GDP.MKTP.CD",
    "idh": "https://api.example.com/idh",
    # Continue mapeando os outros indicadores...
}

def fetch_indicator_data(indicator_name):
    """
    Busca dados de um indicador específico a partir da URL definida no mapeamento.
    """
    api_url = api_map.get(indicator_name)
    if not api_url:
        raise Exception(f"API não encontrada para o indicador: {indicator_name}")
    
    logger.info(f"Buscando dados do indicador: {indicator_name}")
    for tentativa in range(3):
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                logger.info(f"Sucesso na requisição para {indicator_name}")
                return response.json()
            else:
                logger.warning(f"Tentativa {tentativa+1} falhou para {indicator_name}. Código: {response.status_code}")
        except Exception as e:
            logger.error(f"Tentativa {tentativa+1} - Erro: {e}")
        time.sleep(3)
    raise Exception(f"Falha ao buscar dados para {indicator_name} após 3 tentativas")

def process_indicator_data(indicator_name, raw_data):
    """
    Processa os dados brutos de um indicador e retorna uma estrutura padronizada.
    """
    logger.info(f"Processando dados para o indicador: {indicator_name}")
    processed_data = {}
    for item in raw_data:
        processed_data[item.get("country")] = {
            "valor": item.get("value"),
            "ano": item.get("date"),
            "unidade": item.get("unit", "N/A")
        }
    return processed_data

def save_indicator_data(indicator_name, category_name, data):
    """
    Salva os dados de um indicador específico em um arquivo JSON separado.
    """
    path = f"data/raw/{category_name}/{indicator_name}.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info(f"Dados do indicador {indicator_name} salvos em {path}")

if __name__ == "__main__":
    try:
        logger.info("Iniciando pipeline de ETL...")

        for category, indicators in indicators_config.items():
            logger.info(f"Categoria: {category}")
            for indicator in indicators:
                logger.info(f"Processando indicador: {indicator}")
                
                # Buscar os dados do indicador
                raw_data = fetch_indicator_data(indicator)
                
                # Processar os dados
                processed_data = process_indicator_data(indicator, raw_data)
                
                # Salvar os dados
                save_indicator_data(indicator, category, processed_data)
        
        logger.info("Pipeline concluído com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao executar pipeline: {e}")
