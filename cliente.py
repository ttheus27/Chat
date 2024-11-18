import socket
import threading

# Função para receber mensagens do servidor
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(2048).decode()
            print(message)
        except:
            print("Conexão perdida com o servidor.")
            client_socket.close()
            break

# Função principal para enviar mensagens
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect(('localhost', 7777))  # Endereço IP do servidor e porta
    except:
        return print("Não foi possível se conectar ao servidor.")

    # Inicia uma thread para receber mensagens do servidor
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Recebe o nome de usuário e envia ao servidor
    username = input("")
    client_socket.send(username.encode())

    print("\nPara enviar uma mensagem privada, use o comando: /msg <username> <mensagem>")
    print("Para sair do chat, use o comando: /sair")

    while True:
        message = input()

        if message.lower() == "/sair":
            client_socket.send("/sair".encode())
            print("Você saiu do chat.")
            client_socket.close()
            break
        else:
            # Envia a mensagem ao servidor
            client_socket.send(message.encode())

# Executa o programa do cliente
main()
