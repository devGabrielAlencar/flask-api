import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME"),
    # Usa 3306 se DB_PORT não estiver definida
    'port': int(os.getenv("DB_PORT"))
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
