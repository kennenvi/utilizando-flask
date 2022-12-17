from flask import Flask, render_template
from classes.jogo import Jogo

app = Flask(__name__)

@app.route('/inicio')
def ola():

    jogo1 = Jogo('Persona 5', 'JRPG', 'Playstation 4')
    jogo2 = Jogo('God of War', 'Aventura', 'Plastation 4')
    jogo3 = Jogo('Halo', 'FPS', 'Xbox')

    lista_jogos = [jogo1, jogo2, jogo3]
    return render_template('lista.html', titulo='Jogos', jogos=lista_jogos)

app.run()