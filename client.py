#from lib2to3.pytree import convert
import socket
import sys
import _thread
import json
import os
import time
import zmq

IP_ADDRESS = '127.0.0.1'
TOPIC = None
fila_msgs = []

conf = []
# Envia os dados
def enviar():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUB)
    sock.connect(f"tcp://{IP_ADDRESS}:5500")
    codigo = 5

    # Executa uma acao de acordo com o codigo informado
    while True:
        if(len(fila_msgs) == 0):
            pass
        else:
            data = fila_msgs.pop(0)
            data_converted = json.loads(data)
            codigo = data_converted['codigo']

        if(codigo == 1):
            msg_json = data
            TOPIC = 'login'       
            sock.send_string(f"{TOPIC}", flags=zmq.SNDMORE)
            sock.send_json(msg_json) 
            codigo = 5

        if (codigo == 2):
            msg_json = data
            TOPIC = 'cadastrar'       
            sock.send_string(f"{TOPIC}", flags=zmq.SNDMORE)
            sock.send_json(msg_json)
            codigo = 5
        if codigo == 4 :
            msg_json = data
            TOPIC = 'usuario'       
            sock.send_string(f"{TOPIC}", flags=zmq.SNDMORE)
            sock.send_json(msg_json)
            codigo = 5
        if codigo == 9:
            msg_json = data
            TOPIC = 'pedirListaAnuncios'       
            sock.send_string(f"{TOPIC}", flags=zmq.SNDMORE)
            sock.send_json(msg_json)
            codigo = 5
        if codigo == 10:
            msg_json = data
            TOPIC = 'anuncio'       
            sock.send_string(f"{TOPIC}", flags=zmq.SNDMORE)
            sock.send_json(msg_json)
            codigo = 5

# Recebe a confirmacao do broker
def receberConfirmacao():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.SUB)
    sock.connect(f"tcp://{IP_ADDRESS}:5501")
    while True:
            TOPIC = 'confirmacao'
            sock.subscribe(f"{TOPIC}")
            msg_string = sock.recv_string()
            msg_json = sock.recv_json()
            #print(msg_json)

            # Dados da confirmacao
            data = msg_json
            data_converted = json.loads(data)
            codigo = data_converted['codigo']
            codigo2 = data_converted['codigo2']
            confirmacao = data_converted['confirmacao']

            # Adiciona a confirmacao
            conf.append(confirmacao)

# Recebe a lista de anuncios
def receberAnuncios():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.SUB)
    sock.connect(f"tcp://{IP_ADDRESS}:5501")
    while True:
        # Recebe os dados do usuario
        TOPIC = 'anuncios'
        sock.subscribe(f"{TOPIC}")
        msg_string = sock.recv_string()
        msg_json = sock.recv_json()
        #print(msg_json)

        # Mostra os dados do usuario
        data = msg_json
        anuncios = json.loads(data) 
        os.system('clear') or None

        for anuncio in anuncios:
            print("================================")
            print('Anuncio ID: ', anuncio['id'])
            print('Produto ID: ', anuncio['produto_id'])
            print('Descricao: ', anuncio['descricao'])
            print('De cliente: ', anuncio['de_cliente'])
            print('Data: ', anuncio['data'])
            print("================================")

# Recebe o perfil
def verPerfil():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.SUB)
    sock.connect(f"tcp://{IP_ADDRESS}:5501")
    while True:
        # Recebe os dados do usuario
        TOPIC = 'dados_usuario'
        sock.subscribe(f"{TOPIC}")
        msg_string = sock.recv_string()
        msg_json = sock.recv_json()
        #print(msg_json)

        # Mostra os dados do usuario
        data = msg_json
        converted = json.loads(data) 
        nome =  converted['nome']
        dataNasc = converted['nascimento']
        cpf = converted['cpf']
        email = converted['email'] 
        senha = converted['senha']
        os.system('clear') or None

        print("================================")
        print("Nome : " + nome)
        print("Data de Nascimento : " + dataNasc)
        print("CPF : " + cpf)
        print("Email : " + email)
        print("Senha : " + senha)
        print("================================")

# Roda o menu
def client():
    _thread.start_new_thread(enviar,())
    _thread.start_new_thread(receberConfirmacao,())
    _thread.start_new_thread(verPerfil,())

    ri = 'nao'
    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUB)
    sock.connect(f"tcp://{IP_ADDRESS}:5500")
    opc = None
    #time.sleep(20)

    while opc != "4" :
        os.system('clear') or None
        print("================================")
        print("         1 - Logar")
        print("         2 - Criar Conta")
        print("         4 - Sair")
        print("================================")

        opc = input('Digite uma Opcao: ')
        if opc == '1' :
            os.system('clear') or None
            email = input("Digite o email: ")
            senha = input("Digite a senha: ")
            msg= {}
            msg ['codigo'] = 1
            msg ['codigo2'] = 1
            msg ['email'] = email
            msg ['senha'] = senha   
            msg_json = json.dumps(msg)
            fila_msgs.append(msg_json) 
        if opc == '2':
            os.system('clear') or None
            nome = input("Digite o seu nome: ")
            nascimento = input("Digite sua data Nascimento: ")
            endereco = input("Digite seu endere??o: ")
            cpf = input("Digite seu cpf: ")
            email = input("Digite seu Email: ")
            senha = input("Digite sua senha: ")
            msg= {}
            msg ['codigo'] = 2
            msg ['codigo2'] = 2
            msg ['nome'] = nome
            msg ['nascimento'] = nascimento
            msg ['endereco'] = endereco
            msg ['cpf'] = cpf
            msg ['email'] = email
            msg ['senha'] = senha

            msg_json = json.dumps(msg)
            fila_msgs.append(msg_json)

        
if __name__ == "__main__":
    client()