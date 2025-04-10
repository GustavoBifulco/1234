import sqlite3
import os

def init_db(db_path="data/geoloop.db"):
    # Cria a pasta se necessário
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS paises (
            nome TEXT PRIMARY KEY,
            capital TEXT,
            populacao INTEGER,
            continente TEXT
        )
        """
    )
    conn.commit()
    return conn

def save_to_db(data, conn):
    cursor = conn.cursor()
    for pais, info in data.items():
        cursor.execute(
            """
            INSERT INTO paises (nome, capital, populacao, continente)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(nome) DO UPDATE SET
                capital=excluded.capital,
                populacao=excluded.populacao,
                continente=excluded.continente
            """,
            (pais, info.get("capital"), info.get("populacao"), info.get("continente"))
        )
    conn.commit()
