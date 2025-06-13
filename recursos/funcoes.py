import os, time
import json
from datetime import datetime

def inicializarBancoDeDados():
    # r - read, w - write, a - append
    try:
        banco = open("log.dat","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("log.dat","w")
    
def escreverDados():
    # INI - inserindo no arquivo
    banco = open("log.dat","r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}
        
    data_br = datetime.now().strftime("%d/%m/%Y")
    dadosDict[nome] = (score, data_br)
    
    banco = open("log.dat","w")
    banco.write(json.dumps(dadosDict))
    banco.close()
    
    # END - inserindo no arquivo