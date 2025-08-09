from flask import Blueprint, jsonify, request
from models.db import get_db_connection

livros_bp = Blueprint("livros", __name__)


@livros_bp.route("/livros", methods=["GET"])
def livros_json():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT l.nome AS livro, a.nome AS autor "
        "FROM tb_livros l "
        "JOIN tb_autores a ON l.autor = a.id"
    )
    livros = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(livros)


@livros_bp.route("/livro", methods=["POST"])
def cadastrar_livro():
    if request.is_json:
        data = request.get_json()
        nome = data.get("nome")
        autor_id = data.get("autor")
    else:
        nome = request.form.get("nome")
        autor_id = request.form.get("autor")

    if not nome or not autor_id:
        return jsonify({"error": "Nome do livro e autor são obrigatórios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # O método cursor.execute() sempre retorna None

        # verifica se autor existe
        cursor.execute("SELECT id FROM tb_autores WHERE id = %s", (autor_id,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Autor não encontrado"}), 404

        # verifica se livro existe
        cursor.execute("SELECT nome FROM tb_livros WHERE nome = %s", (nome,))
        livro_duplicado = cursor.fetchone()
        if livro_duplicado:
            return jsonify({"error": "Livro já cadastrado"}), 400

        cursor.execute(
            "INSERT INTO tb_livros (nome, autor) VALUES (%s, %s)", (nome, autor_id)
        )
        conn.commit()
        livro_id = cursor.lastrowid
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"id": livro_id, "message": "Livro cadastrado com sucesso"}), 201
