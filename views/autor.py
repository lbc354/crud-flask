from flask import Blueprint, request, jsonify
from models.db import get_db_connection

autor_bp = Blueprint("autor", __name__)


@autor_bp.route("/autores", methods=["GET"])
def autores_json():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT a.nome AS autor, a.id AS autor_id FROM tb_autores a")
    autores = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(autores)


@autor_bp.route("/autor", methods=["POST"])
def cadastrar_autor():
    if request.is_json:
        data = request.get_json()
        nome = data.get("nome")
    else:
        nome = request.form.get("nome")

    if not nome:
        return jsonify({"error": "Nome do autor é obrigatório"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # verifica se autor existe
        cursor.execute("SELECT nome FROM tb_autores WHERE nome = %s", (nome,))
        autor_duplicado = cursor.fetchone()
        if autor_duplicado:
            return jsonify({"error": "Autor já cadastrado"}), 400

        cursor.execute("INSERT INTO tb_autores (nome) VALUES (%s)", (nome,))
        conn.commit()
        autor_id = cursor.lastrowid
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Autor cadastrado com sucesso", "id": autor_id}), 201
