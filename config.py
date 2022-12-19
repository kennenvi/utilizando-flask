with open('security/secret_key.txt') as f:
    SECRET_KEY = f.read()
with open('security/bd.txt') as f:
    senha = f.read()

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = senha,
        servidor = 'localhost',
        database = 'jogoteca'
    )