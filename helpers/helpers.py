import os
from app import app
import time


def recupera_imagem(id:int):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo
    
    return 'capa_padrao.jpg'

# def salva_imagem(nome_arquivo:str, id:int):
#     upload_path = app.config['UPLOAD_PATH']
#     timestamp = time.time()
#     arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')