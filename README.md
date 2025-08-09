# documentações
https://flask.palletsprojects.com/en/stable/
https://getbootstrap.com/

# no diretório raiz do projeto
python -m venv venv
venv\Scripts\activate
python.exe -m pip install --upgrade pip

# o que instalar
pip install flask mysql-connector-python

# como rodar
flask run (se o nome do arquivo principal for IGUAL a app.py ou wsgi.py)
flask --app <nome_do_arquivo> run (se o nome do arquivo principal for DIFERENTE de app.py ou wsgi.py)

# rotas
http://127.0.0.1:5000/ -> index.html
http://127.0.0.1:5000/authors -> autores.html
http://127.0.0.1:5000/livros -> json[GET]
http://127.0.0.1:5000/livro -> [POST]
http://127.0.0.1:5000/autores -> json[GET]
http://127.0.0.1:5000/autor -> [POST]