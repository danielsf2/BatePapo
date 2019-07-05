import threading
import socket
import ssl
import os
import sys
import platform
import time

def remetente(remetenteName, destinatarioName):
    remetentePort = 31000
    remetenteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    locations = "/home/Aluno/Desktop/BatePapoFinal/CA/demoCA/cacert.pem"

    contexto = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    contexto.load_verify_locations(locations)
    remetenteSocketSSL = contexto.wrap_socket(remetenteSocket, server_hostname=destinatarioName)
    executando = 1

    mensagem = input("\n({}) send to => ({}) : ".format(remetenteName,destinatarioName))

    if(mensagem == ""):
        mensagem = "Empty message!"

    try:
        remetenteSocketSSL.connect((destinatarioName, remetentePort))

    except Exception as e:
        print("=> Problema com o host indicado! <=")
        sys.exit(0)

    else:

        if mensagem == "SAIR":
            print("Conexão Encerrada!")
            remetenteSocketSSL.send(mensagem.encode('utf-8'))
            executando = remetenteSocketSSL.recv(2048)
            executando = 0
            remetenteSocketSSL.close()

        else:
            remetenteSocketSSL.send(mensagem.encode('utf-8'))

        while executando == 1:
            mensagem = input("\n({}) send => ({}) : ".format(remetenteName,destinatarioName))

            if(mensagem == ""):
                    mensagem = "Empty message!"

            if mensagem == "SAIR":
                print("Conexão Encerrada!")
                remetenteSocketSSL.send(mensagem.encode('utf-8'))
                executando = remetenteSocketSSL.recv(2048)
                executando = 0
                remetenteSocketSSL.close()

            else:
                remetenteSocketSSL.send(mensagem.encode('utf-8'))

def destinatario(socketConexao, enderecoCliente):
    executando = 1
    destinatarioNome = platform.node()

    while executando == 1:
        mensagem = socketConexao.recv(2048)
        mensagem = mensagem.decode('utf-8')

        if mensagem == "SAIR":
            socketConexao.send(mensagem.encode('utf-8'))
            executando = 0
            print("Seu destinatário se desconectou!!\nDigite \"SAIR\" para finalizar a seção!")
            socketConexao.close()

        else:
            remetente = enderecoCliente[0]
            remetente = remetente.split('.')
            remetente = "b7host" + remetente[2]
            print("\n{} <==== from ({}) : {}".format(enderecoCliente,destinatarioNome, mensagem))


def main():
    destinatarioPort = 31000
    destinatarioSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    destinatarioSocket.bind(("", destinatarioPort))
    destinatarioSocket.listen(0)

    contexto = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    remetenteName = platform.node()

    print("\n\nSua máquina é: {}".format(remetenteName))

    destinatarioName = input("\nDestinatário : ")

    cert = "/home/Aluno/Desktop/BatePapoFinal/CertificadoSSL/"+remetenteName+"/certificado-"+remetenteName+".pem"
    key = "/home/Aluno/Desktop/BatePapoFinal/CertificadoSSL/"+remetenteName+"/privada-"+remetenteName+".pem"

    contexto.load_cert_chain(certfile=cert,keyfile=key)

    destinatarioSocketSSL = contexto.wrap_socket(destinatarioSocket, server_side=True)

    threadRemetente = threading.Thread(target=remetente, args=(remetenteName,destinatarioName))
    threadRemetente.start()

    socketConexao,enderecoCliente = destinatarioSocketSSL.accept()
    threadDestinatario = threading.Thread(target=destinatario, args=(socketConexao,enderecoCliente))
    threadDestinatario.start()

if __name__ == '__main__':
    main()
