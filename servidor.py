import threading
import socket

# Dicionários para gerenciar clientes conectados e nomes de usuários
clients = {}
usernames = {}

# Função para lidar com as mensagens de um cliente
def handle_client(client, client_addr):
    # Solicita o nome de usuário do cliente assim que ele se conecta
    client.send("Digite seu nome de usuário: ".encode())
    username = client.recv(2048).decode().strip()
    usernames[client] = username
    clients[client] = client_addr
    print(f"{username} se juntou ao chat com o código {client_addr}")
    broadcast(f"{username} entrou no chat.", None)

    while True:
        try:
            msg = client.recv(2048).decode().strip()
            if msg:
                # Verifica se é uma mensagem privada
                if msg.startswith("/msg"):
                    parts = msg.split(" ", 2)
                    if len(parts) < 3:
                        client.send("Comando inválido! Use: /msg <username> <mensagem>".encode())
                    else:
                        _, target_username, private_msg = parts
                        send_private_message(client, target_username, private_msg)
                else:
                    # Transmite a mensagem para todos os clientes (mensagem pública)
                    broadcast(f"{username}: {msg}", client)
        except:
            # Remove o cliente em caso de erro
            remove_client(client)
            break

# Função para transmitir mensagens para todos os clientes
def broadcast(msg, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(msg.encode())
            except:
                remove_client(client)

# Função para enviar uma mensagem privada
def send_private_message(sender, target_username, message):
    sender_username = usernames[sender]
    for client, username in usernames.items():
        if username == target_username:
            try:
                client.send(f"[Mensagem privada de {sender_username}]: {message}".encode())
                sender.send(f"[Para {target_username}]: {message}".encode())
            except:
                remove_client(client)
            return
    # Se o usuário alvo não for encontrado
    sender.send("Usuário não encontrado!".encode())

# Função para remover um cliente da lista
def remove_client(client):
    if client in clients:
        username = usernames[client]
        # Remove o cliente da lista e dos dicionários
        del usernames[client]
        del clients[client]
        client.close()
        print(f"{username} saiu do chat.")
        broadcast(f"{username} saiu do chat.", None)


# Função principal para inicializar o servidor
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Iniciou o servidor de bate-papo")

    try:
        server.bind(('0.0.0.0', 7777))
        server.listen()
    except:
        return print('\nNão foi possível iniciar o servidor!\n')

    while True:
        client, addr = server.accept()
        #print(f"Cliente conectado com sucesso. IP: {addr}")
        # Inicia uma nova thread para lidar com as mensagens do cliente
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()

# Executa o programa
main()
