import os
import mysql.connector
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

# Usa DATABASE_URL se existir, senão cai no modo tradicional
database_url = os.getenv("DATABASE_URL")

if database_url:
    url = urlparse(database_url)
    db_config = {
        'host': url.hostname,
        'user': url.username,
        'password': url.password,
        'database': url.path[1:],  # remove a "/" do início
        'port': url.port or 3306
    }
else:
    db_config = {
        'host': os.getenv("DB_HOST", "localhost"),
        'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD"),
        'database': os.getenv("DB_NAME"),
        'port': int(os.getenv("DB_PORT", 3306))
    }


def listar_clientes():
    conexao = mysql.connector.connect(**db_config)
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    cursor.close()
    conexao.close()
    return clientes


def adicionar_clientes(cliente):
    conexao = mysql.connector.connect(**db_config)
    cursor = conexao.cursor()
    sql = """
        INSERT INTO clientes (nome, endereco, bairro, telefone, suco_preferido, obs)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (
        cliente.get("nome"),
        cliente.get("endereco"),
        cliente.get("bairro"),
        cliente.get("telefone"),
        cliente.get("suco_preferido"),
        cliente.get("obs", "")
    )
    cursor.execute(sql, valores)
    conexao.commit()
    cursor.close()
    conexao.close()
