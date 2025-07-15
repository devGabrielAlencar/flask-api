import mysql.connector


db_config = {
    'host': "localhost",
    'user': "root",
    'password': "ga1998",
    'database': "crm"
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
        INSERT INTO clientes (nome,endereco,bairro,telefone,suco_preferido,obs)
        VALUES(%s,%s,%s,%s,%s,%s)
    """

    valores = (
        cliente.get("nome"),
        cliente.get("endereco"),
        cliente.get("bairro"),
        cliente.get("telefone"),
        cliente.get("suco"),
        cliente.get("obs", "")
    )

    cursor.execute(sql, valores)
    conexao.commit()
    cursor.close()
    conexao.close()
