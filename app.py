from flask import Flask, render_template
from views.livros import livros_bp
from views.autor import autor_bp

app = Flask(__name__)

# blueprints
app.register_blueprint(livros_bp)
app.register_blueprint(autor_bp)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/authors")
def autores():
    return render_template("autores.html")


if __name__ == "__main__":
    app.run(debug=True)
