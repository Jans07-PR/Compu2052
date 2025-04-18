from flask import Flask, render_template

app = Flask(__name__)

videojuegos = [
    {"titulo": "The Legend of Zelda: Breath of the Wild", "plataforma": "Nintendo Switch", "genero": "Aventura"},
    {"titulo": "God of War Ragnarök", "plataforma": "PlayStation 5", "genero": "Acción"},
    {"titulo": "Hollow Knight", "plataforma": "PC", "genero": "Metroidvania"}
]



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/juegos')
def mostrar_juegos():
    return render_template('juegos.html', juegos=videojuegos)

if __name__ == '__main__':
    app.run(debug=True)