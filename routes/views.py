from flask import render_template, url_for, flash, request, session, redirect
from app import app, db
from models.models import Jogos, Usuarios


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

    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('Jogo já está cadastrado')
        return redirect(url_for('index'))
    
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

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
            session['usuario_logado'] = usuario.apelido
            flash(usuario.apelido + ' logado com sucesso')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)

    flash('Usuário ou senha inválidos')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('index'))