#from re import T
#from contextlib import ContextDecorator
import socket
import _thread
import json
from time import time
import zmq
import sys
import time
from sqlalchemy.orm import sessionmaker
from db import *

IP_ADDRESS = '10.0.1.1'
TOPIC = None
fila_msgs = []

# Recebe os dados do cliente e passa para o broker
def usuario():
    while True:
        # Contexto do broker
        ctx = zmq.Context()
        sock = ctx.socket(zmq.SUB)
        sock.connect(f"tcp://{IP_ADDRESS}:5501")
    
        # Recebe os dados de perfil do broker
        TOPIC = 'usuario'
        sock.subscribe(f"{TOPIC}")
        msg_string = sock.recv_string()
        msg_json = sock.recv_json()

        # Le o arquivo MUDAR ISSO
        print(msg_json)
        data_converted = json.loads(msg_json)
        codigo = data_converted['codigo']
        email = data_converted['emaill']
        arquivo = open('cadastro.txt', 'r')
        email = '"' + email + '"' + ','
        #print(email)
        
        for linha in arquivo:
            val = linha.split()
            #print(val[11])
            if (email == val[11] ):
                print(val[11])
                msg= {}
                msg ['codigo'] = 6
                msg ['nomee'] = val[5]
                msg ['dataNascimentoo'] = val[7]
                msg ['cpff'] = val[9]
                msg ['emaill'] = val[11]
                msg ['senhaa'] = val[13]
                msg_json = json.dumps(msg)
                fila_msgs.append(msg_json) 

# Envia os dados para o broker
def enviar():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUB)
    sock.connect(f"tcp://{IP_ADDRESS}:5500")
    # Define a variavel codigo
    codigo = 5

    # Envia o dado de acordo com o codigo
    while True:
        if(len(fila_msgs) == 0):
            pass
        else:
            data = fila_msgs.pop(0)
            data_converted = json.loads(data)
            codigo = data_converted['codigo']
        
        if(codigo == 3):
            msg_json = data
            TOPIC = 'confirmacao'     
            sock.send_string(f"{TOPIC}", flags=zmq.SNDMORE)
            sock.send_json(msg_json) 
            codigo = 5
        if(codigo == 6):
            msg_json = data
            TOPIC = 'enviarpefil'    
            sock.send_string(f"{TOPIC}", flags=zmq.SNDMORE)
            sock.send_json(msg_json) 
            codigo = 5
        if(codigo == 8):
            msg_json = data
            TOPIC = 'enviarlista'    
            sock.send_string(f"{TOPIC}", flags=zmq.SNDMORE)
            sock.send_json(msg_json) 
            codigo = 5
        if(codigo == 9):
            msg_json = data
            TOPIC = 'enviarcontrrr'   
            sock.send_string(f"{TOPIC}", flags=zmq.SNDMORE)
            sock.send_json(msg_json) 
            codigo = 5 
        if codigo == 15:
            msg_json = data
            TOPIC = 'finalizar'   
            sock.send_string(f"{TOPIC}", flags=zmq.SNDMORE)
            sock.send_json(msg_json) 
            codigo = 5 
        if(codigo == 11):
            msg_json = data
            TOPIC = 'finalizar'       
            sock.send_string(f"{TOPIC}", flags=zmq.SNDMORE)
            sock.send_json(msg_json) 
            codigo = 5
def login():
    while True:
        ctx = zmq.Context()
        sock = ctx.socket(zmq.SUB)
        sock.connect(f"tcp://{IP_ADDRESS}:5501")

        # Recebe os dados de login do broker
        cont = 1
        TOPIC = 'login'
        sock.subscribe(f"{TOPIC}")
        msg_string = sock.recv_string()
        msg_json = sock.recv_json()

        # Obtem o email e a senha atraves do arquivo
        print(msg_json)
        converted = json.loads(msg_json)

        # Cria o objeto da secao
        Session = sessionmaker(bind=engine)
        session = Session()

        # Obtem os resultados de acordo com o email e senha
        cliente = session.query(User).filter_by(nome=converted['nome'], senha=converted['senha']).all()

        print("Cliente logado")
        print(cliente)

def cadastrar():
    while True:
        # Contexto do broker
        ctx = zmq.Context()
        sock = ctx.socket(zmq.SUB)
        sock.connect(f"tcp://{IP_ADDRESS}:5501")

        # Cadastro dos dados
        TOPIC = 'cadastrar'
        sock.subscribe(f"{TOPIC}")
        msg_string = sock.recv_string()
        msg_json = sock.recv_json()
        converted = json.loads(msg_json)
        print(msg_json)

        # Cria o objeto da secao
        Session = sessionmaker(bind=engine)
        session = Session()

        # Adiciona o cliente
        cliente = Cliente(nome=converted['nome'], cpf=converted['cpf'], email=converted['email'], nascimento=converted['nascimento'], endereco=converted['endereco'], senha=converted['senha'])
        # Insere o cliente
        session.add(cliente)
        session.commit()

# Cria um novo produto
def produto():
    while True:
        # Contexto do broker
        ctx = zmq.Context()
        sock = ctx.socket(zmq.SUB)
        sock.connect(f"tcp://{IP_ADDRESS}:5501")

        # Cadastro dos dados
        TOPIC = 'produto'
        sock.subscribe(f"{TOPIC}")
        msg_string = sock.recv_string()
        msg_json = sock.recv_json()
        converted = json.loads(msg_json)
        print(msg_json)

        # Cria o objeto da secao
        Session = sessionmaker(bind=engine)
        session = Session()

        # Adiciona o produto
        produto = Produto(cliente_id=converted['cliente_id'], nome=converted['nome'], descricao=converted['descricao'], preco=converted['preco'])
        # Insere o produto
        session.add(produto)
        session.commit()

# Adiciona um produto no carrinho
def carrinho():
    while True:
        # Contexto do broker
        ctx = zmq.Context()
        sock = ctx.socket(zmq.SUB)
        sock.connect(f"tcp://{IP_ADDRESS}:5501")

        # Cadastro dos dados
        TOPIC = 'carrinho'
        sock.subscribe(f"{TOPIC}")
        msg_string = sock.recv_string()
        msg_json = sock.recv_json()
        converted = json.loads(msg_json)
        print(msg_json)

        # Cria o objeto da secao
        Session = sessionmaker(bind=engine)
        session = Session()

        # Adiciona o produto
        produto = Produto(cliente_id=converted['cliente_id'], nome=converted['nome'], descricao=converted['descricao'], quantidade=converted['quantidade'])
        # Insere o produto
        session.add(produto)
        session.commit()

# Cria anuncio de produto
def anuncio():
    while True:
        # Contexto do broker
        ctx = zmq.Context()
        sock = ctx.socket(zmq.SUB)
        sock.connect(f"tcp://{IP_ADDRESS}:5501")

        # Cadastro dos dados
        TOPIC = 'anuncio'
        sock.subscribe(f"{TOPIC}")
        msg_string = sock.recv_string()
        msg_json = sock.recv_json()
        converted = json.loads(msg_json)
        print(msg_json)

        # Cria o objeto da secao
        Session = sessionmaker(bind=engine)
        session = Session()

        # Adiciona o anuncio
        anuncio = Anuncio(produto_id=converted['produto_id'], descricao=converted['descricao'], de_cliente=converted['de_cliente'], data=converted['data'])
        
        # Insere o anuncio
        session.add(anuncio)
        session.commit()

def confirmarTroca():
    while True:
        ctx = zmq.Context()
        sock = ctx.socket(zmq.SUB)
        sock.connect(f"tcp://{IP_ADDRESS}:5501")
    
        TOPIC = 'confirmacao'
        sock.subscribe(f"{TOPIC}")
        msg_string = sock.recv_string()
        msg_json = sock.recv_json()
        converted = json.loads(msg_json)
        print(msg_json)

        # Cria o objeto da secao
        Session = sessionmaker(bind=engine)
        session = Session()

        # Adiciona o troca
        troca = Troca(anuncio=converted['anuncio'], para_cliente=converted['para_cliente'])
        
        # Insere o troca
        session.add(troca)
        session.commit()


def server():
    _thread.start_new_thread(cadastrar,())
    _thread.start_new_thread(login,())
    _thread.start_new_thread(enviar,()) # Refatorar
    _thread.start_new_thread(usuario,()) # Refatorar
    _thread.start_new_thread(produto, ())
    _thread.start_new_thread(carrinho, ())
    _thread.start_new_thread(anuncio, ())
    _thread.start_new_thread(confirmarTroca, ())

    while True:
        pass

if __name__ == "__main__":
    server()