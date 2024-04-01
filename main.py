import socket
import json
import threading
from ficheiro import *

HOST = 'localhost'
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []


def gerir_clientes(client_socket, client_address):
    print(f'Novo cliente conectado: {client_address}.')

    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                gerir_mensagens(message, client_address, client_socket)
            else:
                remove_client(client_socket)
                break
        except Exception as e:
            print(f'Erro ao lidar com a conexão do cliente {client_address}: {e}')
            remove_client(client_socket)
            break


def gerir_mensagens(mensagem, client_address, client_socket):
    # Converter os dados de JSON para um dicionário
    dados = json.loads(mensagem)
    primeiro_dados = iter(dados.items())
    primeiro_item = next(primeiro_dados)
    # Nova conta
    if primeiro_item[0] == 'novo_mail':
        print("Dados recebidos do cliente: ", client_address)
        nova_conta((dados['novo_mail'][2:-1]),(dados['nova_pass'][2:-1]), (dados['nome_utilizador']))
    if primeiro_item[0] == 'email':
        print("Dados recebidos do cliente: ", client_address)
        resp, nome = verifica_conta((dados['email'][2:-1]), (dados['password'][2:-1]))
        if resp == 'True':
            clients.append(client_socket)
        dados_envio = {'encontrado': resp, 'nome': nome}
        dados_enviar = json.dumps(dados_envio).encode('utf-8')
        client_socket.send(dados_enviar)
    if primeiro_item[0] == 'mensagem':
        contar = 0
        for client in clients:
            if client != client_socket:
                client.send(json.dumps(dados).encode('utf-8'))
                contar += 1
        print(f'Mensagem recebida de {client_address} e enviada para {contar} clientes')
    if primeiro_item[0] == 'remover':
        remove_client(client_socket)
        print(f'Cliente Removido: {client_address}.')


def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()


def main():
    print(f'Servidor de chat está ativo em {HOST}:{PORT}')

    while True:
        client_socket, client_address = server.accept()
        threading.Thread(target=gerir_clientes, args=(client_socket, client_address)).start()


if __name__ == "__main__":
    main()
