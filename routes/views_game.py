from flask import render_template, url_for, flash, request, session, redirect, send_from_directory
from markupsafe import escape
from app import app, db
from models.models import Jogos
from helpers.helpers import recupera_imagem, deleta_arquivo, FormularioJogo
import time


@app.route('/')
def index():
    # Listando os jogos
    lista_jogos = Jogos.query.order_by(Jogos.id)
    return render_template('index.html', titulo='Jogos', jogos=lista_jogos)

@app.route('/novo')
def novo():
    # Verificando se o usuário está logado
    if 'usuario_logado' not in session:
        flash('Faça login para continuar')
        return redirect(url_for('login', proxima=url_for('novo')))
    
    # Caso usuário esteja logado
    form = FormularioJogo()
    return render_template('novo.html', titulo='Novo Jogo', form=form)

@app.post('/criar')
def criar():
    form = FormularioJogo()

    # Validando formulário
    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    # Atribuições
    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    # Verificando se o jogo já está cadastrado
    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash('Jogo já está cadastrado')
        return redirect(url_for('index'))
    
    # Criando novo jogo
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    # Salvando imagem
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    # Vericando se o usuário está logado
    if 'usuario_logado' not in session:
        flash('Faça login para continuar')
        return redirect(url_for('login', proxima=url_for('editar')))
    
    form = FormularioJogo()

    # Extraindo dados do banco para preencher o editar
    jogo = Jogos.query.filter_by(id=id).first()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Jogo', id=id, capa_jogo=capa_jogo, form=form)

@app.post('/atualizar')
def atualizar():
    form = FormularioJogo()

    # Validando campos
    if not form.validate_on_submit():
        flash('Não foi possível atualizar')
        return redirect(url_for('editar', id=request.form['id']))

    jogo = Jogos.query.filter_by(id=request.form['id']).first()
    
    # Realiza as modificações
    jogo.nome = form.nome.data
    jogo.categoria = form.categoria.data
    jogo.console = form.console.data
    
    # Commita no banco de dados
    db.session.add(jogo)
    db.session.commit()

    # Altera imagem da capa
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(jogo.id)
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    # Verificando se o usuário está logado
    if 'usuario_logado' not in session:
        flash('Faça login para continuar')
        return redirect(url_for('login'))
    
    # Deletando jogo
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo deletado com sucesso')

    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    # Buscando imagem para colocar no HTML
    return send_from_directory('uploads', escape(nome_arquivo))