from flask import Flask, render_template, request, redirect, session, flash, url_for
from classes.jogo import Jogo
from classes.usuario import Usuario
from flask_sqlalchemy import SQLAlchemy


jogo1 = Jogo('Persona 5', 'JRPG', 'Playstation 4')
jogo2 = Jogo('God of War', 'Aventura', 'Plastation 4')
jogo3 = Jogo('Halo', 'FPS', 'Xbox')

lista_jogos = [jogo1, jogo2, jogo3]

usuario1 = Usuario("Igor Batista", "Igão", "argentina_campea")
usuario2 = Usuario("Ana Letícia", "Leh", "gosto_de_churrasco")
usuario3 = Usuario("Ezio Auditore", "O mio todos", "florenca")

usuarios = {usuario1.apelido: usuario1,
            usuario2.apelido: usuario2,
            usuario3.apelido: usuario3}

app = Flask(__name__)
with open('security/secret_key.txt') as f:
    app.secret_key = f.read()
with open('security/bd.txt') as f:
    senha = f.read()

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = senha,
        servidor = 'localhost',
        database = 'jogoteca'
    )
db = SQLAlchemy(app)

class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    def __repr__(self) -> str:
        return '<Name %r>' % self.nome

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    apelido = db.Column(db.String(8), nullable=False)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return '<Name %r>' % self.nome

# Rotas
@app.route('/')
def index():
    lista_jogos = Jogos.query.order_by(Jogos.id)
    return render_template('index.html', titulo='Jogos', jogos=lista_jogos)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session:
        flash('Faça login para continuar')
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
    usuario = Usuarios.query.filter_by(apelido=request.form['usuario']).first()
    if usuario:
        if usuario.senha == request.form['senha']:
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)

    flash('Usuário ou senha inválidos')
    proxima = request.args.get('proxima')
    if not proxima:
        proxima = url_for('login')
    return redirect(url_for('login', proxima=proxima))

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('index'))

# Rodar o Flask
if __name__ == '__main__':
    app.run(debug=True)