import socket
import threading
import time

clients = []
bancodados = {}

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('localhost', 7777))
        server.listen(10)
    except:
        return print('\nNão foi possível iniciar o servidor')
    
    while True:
        try:
            client, address = server.accept()
            clients.append(client)
        except OSError:
            # Como fechamos o socket na thread para cliente,
            # quando tentarmos escutar no mesmo socket, ele não mais
            # existirá e lançará um erro
            # Não é isso que servidores de verdade fazem, é só um exemplo
            time.sleep(1)
            print(f"Servidor: desligando thread de escuta")
            break

        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()


def messagesTreatment(client):
    while True:
        try:
            msg_bytes = client.recv(2048)
            msg = msg_bytes.decode()
            print(msg)
            listArgs = msg.split(',')
            
            print(listArgs)
            if listArgs[0]=='<sender>':
                
                bancodados[listArgs[1]] = listArgs[2:]
                print(bancodados)
            elif listArgs[0] == '<reciver>':
                
                print(bancodados[listArgs[1]])
                client.send(f"{bancodados[listArgs[1]][0]},{bancodados[listArgs[1]][1]}".encode())
            else:
                break

        except:
            print("algo deu errado")
            break




# def broadcast(msg, client):
#     for clientItem in clients:
#         if clientItem != client:
#             try:
#                 clientItem.send(msg)
#             except:
#                 deleteClient(clientItem)

# def deleteClient(client):
#     clients.remove(client)
main()