#!/usr/bin/env python3
import requests
import json
import os
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def fetch_economic_data(country_code="all", indicator="NY.GDP.MKTP.CD", start_year=2019, end_year=2020):
    """
    Busca dados econômicos (PIB) usando a API do Banco Mundial para todos os países e, em seguida, 
    filtra para manter somente os países membros oficiais da ONU.
    """
    url = (
        f"http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}"
        f"?format=json&date={start_year}:{end_year}&per_page=5000"
    )
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            logger.info("Dados brutos obtidos da API.")
            if len(data) > 1 and data[1]:
                # Lista de códigos ISO3 dos 193 países membros oficiais da ONU
                onu_iso3_codes = [
                    "AFG", "ALB", "DZA", "AND", "AGO", "ATG", "ARG", "ARM", "AUS", "AUT",
                    "AZE", "BHS", "BHR", "BGD", "BRB", "BLR", "BEL", "BLZ", "BEN", "BTN",
                    "BOL", "BIH", "BWA", "BRA", "BRN", "BGR", "BFA", "BDI", "CPV", "KHM",
                    "CMR", "CAN", "CAF", "TCD", "CHL", "CHN", "COL", "COM", "COG", "CRI",
                    "CIV", "HRV", "CUB", "CYP", "CZE", "COD", "DNK", "DJI", "DMA", "DOM",
                    "ECU", "EGY", "SLV", "GNQ", "ERI", "EST", "ETH", "FJI", "FIN", "FRA",
                    "GAB", "GMB", "GEO", "DEU", "GHA", "GRC", "GRD", "GTM", "GIN", "GNB",
                    "GUY", "HTI", "HND", "HUN", "ISL", "IND", "IDN", "IRN", "IRQ", "IRL",
                    "ISR", "ITA", "JAM", "JPN", "JOR", "KAZ", "KEN", "KIR", "KOR", "KWT",
                    "KGZ", "LAO", "LVA", "LBN", "LSO", "LBR", "LBY", "LIE", "LTU", "LUX",
                    "MDG", "MWI", "MYS", "MDV", "MLI", "MLT", "MHL", "MRT", "MUS", "MEX",
                    "FSM", "MDA", "MCO", "MNG", "MNE", "MAR", "MOZ", "MMR", "NAM", "NRU",
                    "NPL", "NLD", "NZL", "NIC", "NER", "NGA", "MKD", "NOR", "OMN", "PAK",
                    "PLW", "PAN", "PNG", "PRY", "PER", "PHL", "POL", "PRT", "QAT", "ROU",
                    "RUS", "RWA", "KNA", "LCA", "VCT", "WSM", "SMR", "STP", "SAU", "SEN",
                    "SRB", "SYC", "SLE", "SGP", "SVK", "SVN", "SLB", "SOM", "ZAF", "SSD",
                    "ESP", "LKA", "SDN", "SUR", "SWE", "CHE", "SYR", "TJK", "TZA", "THA",
                    "TLS", "TGO", "TON", "TTO", "TUN", "TUR", "TKM", "TUV", "UGA", "UKR",
                    "ARE", "GBR", "USA", "URY", "UZB", "VUT", "VEN", "VNM", "YEM", "ZMB",
                    "ZWE"
                ]
                # Filtra os registros: manter somente se o campo "countryiso3code" está na lista
                filtered = [item for item in data[1] if item["countryiso3code"] in onu_iso3_codes]
                logger.info(f"Total de registros após filtragem: {len(filtered)}")
                return filtered
            else:
                logger.warning("Nenhum dado encontrado na resposta da API.")
        else:
            logger.error(f"Erro ao acessar a API. Código: {response.status_code}")
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
    logger.info("Iniciando coleta de dados econômicos para países oficiais da ONU...")
    economic_data = fetch_economic_data()
    save_economic_data(economic_data)
