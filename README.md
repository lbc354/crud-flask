# documentações
https://flask.palletsprojects.com/en/stable/
https://getbootstrap.com/

# preparando ambiente
python -m venv venv
venv\Scripts\activate
python.exe -m pip install --upgrade pip

pip install flask mysql-connector-python
OR
pip install -r requirements.txt

# como rodar
flask run (se o nome do arquivo principal for IGUAL a app.py ou wsgi.py)
flask --app <nome_do_arquivo> run (se o nome do arquivo principal for DIFERENTE de app.py ou wsgi.py)

# rotas
http://127.0.0.1:5000/ -> livros.html
http://127.0.0.1:5000/authors -> autores.html

http://127.0.0.1:5000/livros -> json[GET]
http://127.0.0.1:5000/livro -> [POST]
http://127.0.0.1:5000/livro/_id -> [PATCH]
http://127.0.0.1:5000/livro/_id -> [DELETE]

http://127.0.0.1:5000/autores -> json[GET]
http://127.0.0.1:5000/autor -> [POST]
http://127.0.0.1:5000/autor/_id -> [PATCH]
http://127.0.0.1:5000/autor/_id -> [DELETE]

# sql
CREATE DATABASE IF NOT EXISTS desafio;
USE desafio;

CREATE TABLE tb_autores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE tb_livros (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    autor INT NULL,
    CONSTRAINT fk_livros_autor FOREIGN KEY (autor) REFERENCES tb_autores(id) ON DELETE SET NULL
);