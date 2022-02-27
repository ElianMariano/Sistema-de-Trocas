#from lib2to3.pytree import convert
import socket
import sys
import _thread
import json
import os
import time
import zmq

IP_ADDRESS = '10.0.1.1'
TOPIC = None
fila_msgs = []

conf = []
def enviar():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUB)
    sock.connect(f"tcp://{IP_ADDRESS}:5500")
    codigo = 5
    while True:
        if(len(fila_msgs) == 0):
            pass
        else:
            data = fila_msgs.pop(0)
            data_converted = json.loads(data)
            codigo = data_converted['codigo']

        if(codigo == 1):
            msg_json = data
            TOPIC = 'logar'       
            sock.send_string(f"{TOPIC}", flags=zmq.SNDMORE)
            sock.send_json(msg_json) 
            codigo = 5

        if (codigo == 2):
            msg_json = data
            TOPIC = 'cadastro'       
            sock.send_string(f"{TOPIC}", flags=zmq.SNDMORE)
            sock.send_json(msg_json)
            codigo = 5
        if codigo == 4 :
            msg_json = data
            TOPIC = 'perfil'       
            sock.send_string(f"{TOPIC}", flags=zmq.SNDMORE)
            sock.send_json(msg_json)
            codigo = 5
        if codigo == 7:
            msg_json = data
            TOPIC = 'pedirlistafrutas'       
            sock.send_string(f"{TOPIC}", flags=zmq.SNDMORE)
            sock.send_json(msg_json)
            codigo = 5
        if codigo == 9:
            msg_json = data
            TOPIC = 'comprarfruta'       
            sock.send_string(f"{TOPIC}", flags=zmq.SNDMORE)
            sock.send_json(msg_json)
            codigo = 5
        # fazer
        if codigo == 13:
            msg_json = data
            TOPIC = 'requisitarHist'       
            sock.send_string(f"{TOPIC}", flags=zmq.SNDMORE)
            sock.send_json(msg_json)
            codigo = 5

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
            data = msg_json
            data_converted = json.loads(data)
            codigo = data_converted['codigo']
            codigo2 = data_converted['codigo2']
            confirmacao = data_converted['confirmacao']
            conf.append(confirmacao)

def verPerfil():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.SUB)
    sock.connect(f"tcp://{IP_ADDRESS}:5501")
    while True:
        TOPIC = 'enviarpefil'
        sock.subscribe(f"{TOPIC}")
        msg_string = sock.recv_string()
        msg_json = sock.recv_json()
        #print(msg_json)
        data = msg_json
        data_converted = json.loads(data) 
        nome =  data_converted['nomee']
        dataNasc = data_converted['dataNascimentoo']
        cpf = data_converted['cpff']
        email = data_converted['emaill'] 
        senha = data_converted['senhaa']
        os.system('clear') or None
        print("       lista dos dados do usuario")
        print("Nome : " + nome)
        print("Data de Nascimento : " + dataNasc)
        print("CPF : " + cpf)
        print("Email : " + email)
        print("Senha : " + senha)

def receberLista():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.SUB)
    sock.connect(f"tcp://{IP_ADDRESS}:5501")
    while True:
        TOPIC = 'enviarlista' 
        sock.subscribe(f"{TOPIC}")
        msg_string = sock.recv_string()
        msg_json = sock.recv_json()
        #print(msg_json)
        data = msg_json
        data_converted = json.loads(data) 
        codigo =  data_converted['codigo']
        #pr = data_converted['raa']
        contador = data_converted['contador']
        li = []
        i=0
        vallor = 'val'
        f = int(contador)
        for linha in range(f+1):
            vallor = 'val' + str(i)
            li.append(data_converted[vallor])
            i = i +1
        i=0
        for linha in range(f+1):
            print("Codigo: ",i, "  item: " ,li.pop(0))
            i = i +1

def client():
    _thread.start_new_thread(enviar,())
    _thread.start_new_thread(receberConfirmacao,())
    _thread.start_new_thread(verPerfil,())
    _thread.start_new_thread(receberLista,())

    ri = 'nao'
    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUB)
    sock.connect(f"tcp://{IP_ADDRESS}:5500")
    opc = None
    #time.sleep(20)

    while opc != "4" :
        os.system('clear') or None