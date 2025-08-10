from flask import Blueprint, request, jsonify
from models.db import get_db_connection

autor_bp = Blueprint("autor", __name__)


@autor_bp.route("/autores", methods=["GET"])
def autores_json():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nome FROM tb_autores ORDER BY id DESC")
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

    nome = nome.strip()

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


@autor_bp.route("/autor/<int:autor_id>", methods=["PATCH"])
def editar_autor(autor_id):
    # aceita JSON ou form
    if request.is_json:
        data = request.get_json()
        novo_nome = data.get("nome")
    else:
        novo_nome = request.form.get("nome")

    if not novo_nome:
        return jsonify({"error": "Nome do autor é obrigatório."}), 400

    novo_nome = novo_nome.strip()

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # verifica se autor existe
        cursor.execute("SELECT id FROM tb_autores WHERE id = %s", (autor_id,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Autor não encontrado."}), 404

        # verifica duplicado (exceto o próprio autor)
        cursor.execute(
            "SELECT id FROM tb_autores WHERE nome = %s AND id != %s",
            (novo_nome, autor_id),
        )
        if cursor.fetchone():
            return jsonify({"error": "Outro autor com esse nome já existe."}), 400

        cursor.execute(
            "UPDATE tb_autores SET nome = %s WHERE id = %s", (novo_nome, autor_id)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Autor atualizado com sucesso."}), 200


@autor_bp.route("/autor/<int:autor_id>", methods=["DELETE"])
def excluir_autor(autor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # verificar existência
        cursor.execute("SELECT id FROM tb_autores WHERE id = %s", (autor_id,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Autor não encontrado."}), 404

        # tenta deletar
        try:
            cursor.execute("DELETE FROM tb_autores WHERE id = %s", (autor_id,))
            conn.commit()
        except Exception as e_delete:
            # tenta detectar erro de FK (autor referenciado por livros)
            err_str = str(e_delete).lower()
            if "foreign" in err_str or "constraint" in err_str or "1451" in err_str:
                # código 1451 é MySQL: cannot delete or update a parent row: a foreign key constraint fails
                return (
                    jsonify(
                        {
                            "error": "Não é possível excluir autor porque há livros relacionados."
                        }
                    ),
                    400,
                )
            # erro genérico de delete
            raise

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Autor excluído com sucesso."}), 200
