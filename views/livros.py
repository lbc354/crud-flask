from flask import Blueprint, jsonify, request
from models.db import get_db_connection

livros_bp = Blueprint("livros", __name__)


@livros_bp.route("/livros", methods=["GET"])
def livros_json():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT l.nome AS livro, l.id AS livro_id, a.nome AS autor, a.id AS autor_id "
        "FROM tb_livros l "
        "JOIN tb_autores a ON l.autor = a.id "
        "ORDER BY l.id DESC"
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
        return jsonify({"error": "Nome do livro e autor são obrigatórios."}), 400
    # verifica se autor_id é número inteiro
    try:
        autor_id = int(autor_id)
    except ValueError:
        return jsonify({"error": "Erro ao registrar autor."}), 400

    nome = nome.strip()

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # cursor.execute() sempre retorna None

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


@livros_bp.route("/livro/<int:livro_id>", methods=["PATCH"])
def editar_livro(livro_id):
    data = request.get_json()

    nome = data.get("nome")
    autor_id = data.get("autor")

    if not nome and not autor_id:
        return (
            jsonify(
                {"error": "É necessário informar ao menos um campo para atualizar."}
            ),
            400,
        )

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # verifica se o livro existe
        cursor.execute("SELECT id FROM tb_livros WHERE id = %s", (livro_id,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Livro não encontrado"}), 404

        # Monta a query dinamicamente
        campos = []
        valores = []

        if nome:
            campos.append("nome = %s")
            valores.append(nome.strip())

        if autor_id:
            try:
                autor_id = int(autor_id)
            except ValueError:
                return jsonify({"error": "ID de autor inválido."}), 400

            # verifica se o autor existe
            cursor.execute("SELECT id FROM tb_autores WHERE id = %s", (autor_id,))
            if cursor.fetchone() is None:
                return jsonify({"error": "Autor não encontrado"}), 404

            campos.append("autor = %s")
            valores.append(autor_id)

        valores.append(livro_id)
        sql = f"UPDATE tb_livros SET {', '.join(campos)} WHERE id = %s"
        cursor.execute(sql, tuple(valores))
        conn.commit()

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Livro atualizado com sucesso"}), 200


@livros_bp.route("/livro/<int:livro_id>", methods=["DELETE"])
def excluir_livro(livro_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM tb_livros WHERE id = %s", (livro_id,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Livro não encontrado"}), 404

        cursor.execute("DELETE FROM tb_livros WHERE id = %s", (livro_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Livro excluído com sucesso"}), 200
