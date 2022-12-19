from flask import Flask, render_template, request, redirect, session, flash, url_for
from classes.jogo import Jogo

app = Flask(__name__)
with open('security/secret_key.txt') as f:
    app.secret_key = f.read()

jogo1 = Jogo('Persona 5', 'JRPG', 'Playstation 4')
jogo2 = Jogo('God of War', 'Aventura', 'Plastation 4')
jogo3 = Jogo('Halo', 'FPS', 'Xbox')

lista_jogos = [jogo1, jogo2, jogo3]

# Rotas
@app.route('/')
def index():
    return render_template('index.html', titulo='Jogos', jogos=lista_jogos)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session: #or session['usuario_logado'] == None:
        flash('Por favor, faça login para continuar')
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.post('/criar')
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome, categoria, console)
    lista_jogos.append(jogo)

    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    if not proxima:
        proxima = url_for('index')
    return render_template('login.html', proxima=proxima)

@app.post('/autenticar')
def autenticar():
    if 'alohomora' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        flash(session['usuario_logado'] + ' logado com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    
    flash('Usuario não cadastrado')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

# Rodar o Flask
if __name__ == '__main__':
    app.run(debug=True)