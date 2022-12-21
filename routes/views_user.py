from flask import render_template, url_for, flash, request, session, redirect
from app import app
from models.models import Usuarios
from helpers.helpers import FormularioUsuario


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    if not proxima:
        proxima = url_for('index')
    return render_template('login.html', proxima=proxima, form=form)

@app.post('/autenticar')
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(apelido=form.apelido.data).first()
    if usuario:
        if usuario.senha == form.senha.data:
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