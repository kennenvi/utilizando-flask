from flask import Flask, render_template, request, redirect
from classes.jogo import Jogo

app = Flask(__name__)

jogo1 = Jogo('Persona 5', 'JRPG', 'Playstation 4')
jogo2 = Jogo('God of War', 'Aventura', 'Plastation 4')
jogo3 = Jogo('Halo', 'FPS', 'Xbox')

lista_jogos = [jogo1, jogo2, jogo3]

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista_jogos)

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Jogo')

@app.post('/criar')
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome, categoria, console)
    lista_jogos.append(jogo)

    return redirect('/')


app.run(debug=True)