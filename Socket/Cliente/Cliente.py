# import socket

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# client.connect(('localhost', 7777))
# print("conectado!\n")

# namefile = str(input("Arquivo>"))
# client.send(namefile.encode())

# with open(namefile, 'wb') as file:
#     while True:
#         data = client.recv(1000000)
#         if not data:
#             break
#         file.write(data)

# print(f'{namefile} recebido!\n')

import socket
import threading
        

def main():


    Socketclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    SocketSender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        #portSender = int(input('PortSender:'))
        SocketSender.bind(('localhost',0))
        SocketSender.listen(1)
    except:
        print('não foi possível iniciar o servidor-cliente')

    try:
        Socketclient.connect(('localhost',7777))
    except:
        return print("\nNão foi possível se conectar ao servidor")
    

    print('\nConectado ao servidor')

    thread1 = threading.Thread(target=receiveMenssages,args=[Socketclient])
    thread2 = threading.Thread(target=sendMessages, args=[Socketclient,SocketSender.getsockname()[1]])
    thread3 = threading.Thread(target=servidorSender, args=[SocketSender])
    thread1.start()
    thread2.start()
    thread3.start()


def receiveMenssages(Socketclient):
    while True:
        try:
            msg = Socketclient.recv(2048).decode()
            #print('\n' + msg)

            listargs = msg.split(',')
            startReciver(listargs[0],listargs[1])
        except:
            print('\nNão foi possível se manter conectado no Servidor')
            print('Pressione <Enter> Para continuar')
            Socketclient.close()
            break


def sendMessages(Socketclient,port,key='',ip='localhost'):
    try:
        sender = input("\nDeseja enviar aquivos?(sim)(não)\n")      #solução temporária até receber o frontend
        key = input("\nkey:")
        if sender.lower() =='sim':
            Socketclient.send(f"<sender>,{key},{ip},{port}".encode())
        else:
            Socketclient.send(f"<reciver>,{key}".encode())
    except:
        return



def startReciver(ip,port):
    socketReciver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socketReciver.connect((ip,int(port)))
        namefile = input('\nArquivo:')
        socketReciver.send(namefile.encode())
        while True:
            try:
                with open(namefile,'wb') as file:
                    while True:
                        data = socketReciver.recv(1000000)
                        if not data:
                            break
                        file.write(data)
            except:
                print('\nNão foi possível se manter conectado no Servidor')
                print('Pressione <Enter> Para continuar')
                socketReciver.close()
                break
    except:
        print('não foi possivel se conectar ao servidor cliente')
    

    socketReciver.close()
    return
        


# def sendMenssagesClient(Socketclient,ip, port):
#     try:
#         Socketclient.close()
#         Socketclient.connect((ip,port))
#         print('Conectado ao cliente!')
#         namefile = input('arquivo:')
#         Socketclient.send(namefile.encode())
#         Socketclient.connect(('localhost',7777))
#     except:
#         print("algo deu errado sendMessagesClient")
#         return
    
# def receiveMenssagesClient(Socketservidor):
#     while True:
#         try:
#             namefile = input('Escolha o nome como salvar o arquivo')
#             with open(namefile,'wb') as file:
#                 while True:
#                     data = Socketservidor.recv(1000000)
#                     if not data:
#                         break
#                     file.write(data)

#         except:
#             print('\nNão foi possível se manter conectado no Servidor')
#             print('Pressione <Enter> Para continuar')
#             Socketservidor.close()
#             break



        
def servidorSender(Socketservidor):
    while True:
        try:
            client, address = Socketservidor.accept()
        except OSError:
            # Como fechamos o socket na thread para cliente,
            # quando tentarmos escutar no mesmo socket, ele não mais
            # existirá e lançará um erro
            # Não é isso que servidores de verdade fazem, é só um exemplo
            print(f"Servidor: desligando thread de escuta")
            break
        
        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()

def messagesTreatment(client):
    while True:
        # try: 
            namefile = client.recv(1024).decode()
            with open(namefile,'rb') as file:
                for data in file.readlines():
                    client.send(data)

        # except:
        #     print("algo deu errado messagesTreatment")
        #     break


main()