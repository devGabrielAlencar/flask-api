from flask import Flask, request, jsonify
from bd import adicionar_clientes, listar_clientes
import os

app = Flask(__name__)


@app.route('/clientes', methods=['POST'])
def salvar_cliente():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados JSON são obrigatórios!"}), 400

    if not dados.get("nome") or not dados.get("telefone"):
        return jsonify({"erro": "Nome e telefone são obrigatórios"}), 400

    try:
        adicionar_clientes(dados)
        return jsonify({"mensagem": "Cliente inserido com sucesso"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route('/clientes', methods=['GET'])
def obter_clientes():
    try:
        clientes = listar_clientes()
        return jsonify(clientes), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


if __name__ == "__main__":
    # pega a porta do Heroku ou usa 5000 localmente
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
