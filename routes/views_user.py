from flask import render_template, url_for, flash, request, session, redirect
from markupsafe import escape
from app import app
from models.models import Usuarios
from helpers.formClasses import FormularioUsuario
from flask_bcrypt import check_password_hash


@app.route('/login')
def login():
    # Verificando se o usuário já está logado
    if 'usuario_logado' in session:
        flash('Você já está logado')
        return redirect(url_for('index'))

    form = FormularioUsuario()
    # Verificando qual página o usuário estava para redirecioná-lo após o login
    proxima = request.args.get('proxima')
    proxima = escape(proxima) if proxima else proxima
    
    return render_template('login.html', proxima=proxima, form=form)

@app.post('/autenticar')
def autenticar():
    form = FormularioUsuario()

    # Validando usuário e senha
    usuario = Usuarios.query.filter_by(apelido=form.apelido.data).first()
    if usuario and check_password_hash(usuario.senha, form.senha.data):
        session['usuario_logado'] = usuario.apelido
        flash(usuario.apelido + ' logado com sucesso')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)

    # Caso a senha ou o usuário estejam errados
    proxima_pagina = request.form['proxima']
    flash('Usuário ou senha inválidos')
    return redirect(url_for('login', proxima=proxima_pagina))

@app.route('/logout')
def logout():
    # Retirando o usuario da sessão
    session.pop('usuario_logado', None)
    return redirect(url_for('index'))