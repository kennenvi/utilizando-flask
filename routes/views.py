from flask import render_template, url_for, flash, request, session, redirect, send_from_directory
from app import app, db
from models.models import Jogos, Usuarios
from helpers.helpers import recupera_imagem, deleta_arquivo, FormularioJogo
import time


@app.route('/')
def index():
    lista_jogos = Jogos.query.order_by(Jogos.id)
    return render_template('index.html', titulo='Jogos', jogos=lista_jogos)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session:
        flash('Faça login para continuar')
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioJogo()
    return render_template('novo.html', titulo='Novo Jogo', form=form)

@app.post('/criar')
def criar():
    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('Jogo já está cadastrado')
        return redirect(url_for('index'))
    
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session:
        flash('Faça login para continuar')
        return redirect(url_for('login', proxima=url_for('editar')))
    
    jogo = Jogos.query.filter_by(id=id).first()
    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Jogo', id=id, capa_jogo=capa_jogo, form=form)

@app.post('/atualizar')
def atualizar():
    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        flash('Não foi possível atualizar')
        return redirect(url_for('editar', id=request.form['id']))

    jogo = Jogos.query.filter_by(id=request.form['id']).first()

    jogo.nome = form.nome.data
    jogo.categoria = form.categoria.data
    jogo.console = form.console.data

    db.session.add(jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(jogo.id)
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session:
        flash('Faça login para continuar')
        return redirect(url_for('login'))
    
    jogos = Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo deletado com sucesso')

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

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)