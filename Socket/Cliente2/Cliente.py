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
import os
import datetime
        

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
    flag = False
    try:
        socketReciver.connect((ip,int(port)))
        if not sincronizar(socketReciver):
            flag = True
            return


        os.makedirs('recive',exist_ok=True)
        with socketReciver,socketReciver.makefile('rb') as clientfile: #download em uma pasta local
            while True:
                raw = clientfile.readline()
                if not raw: break # no more files, server closed connection.

                filename = raw.strip().decode()
                length = int(clientfile.readline())

                print(f'Downloading {filename}...\n  Expecting {length:,} bytes...',end='',flush=True)

                path = os.path.join('recive',filename)
                os.makedirs(os.path.dirname(path),exist_ok=True)

                # Read the data in chunks so it can handle large files.
                with open(path,'wb') as f:
                    while length:
                        chunk = min(length,1000000)
                        if not flag:
                            data = clientfile.read(chunk)
                        if not data: break
                        f.write(data)
                        length -= len(data)
                    else: # only runs if while doesn't break and length==0
                        print('Complete')
                        continue

                # socket was closed early.
                print('Incomplete')
                break 
    except:
        print('não foi possivel se conectar ao servidor cliente')
    

    socketReciver.close()
    return
        
def sincronizar(socketReciver):
    listaHash = []
    while True:
        msg = socketReciver.recv(1024).decode()
        if msg == "<END>":
            break
        listaHash.append(msg.split(','))
    
    print('\nimprimindo listahash')
    for hash in listaHash:
        print(hash)

    choice = input("\ndeseja importar o arquivo?(sim)(não)\n")
    if choice == "sim":
        return True
    if choice == "não":
        return False
    print('Algo deu errado na sincronização')
    return

def sendHashlist(client):
    while True:
        for path,dirs,files in os.walk('send'):
            for file in files:
                filename = os.path.join(path,file)
                relpath = os.path.relpath(filename,'send')
                filesize = os.path.getsize(filename)
                # create a file path
                #print(relpath)
                # get creation time on windows
                try:
                    # file modification timestamp of a file
                    m_time = os.path.getmtime(path)
                    # convert timestamp into DateTime object
                    dt_m = datetime.datetime.fromtimestamp(m_time)     
                    # file creation timestamp in float
                    c_time = os.path.getctime(path)
                    # convert creation timestamp into DateTime object
                    dt_c = datetime.datetime.fromtimestamp(c_time)                            
                    client.sendall(f"{relpath},{dt_c},{dt_m}".encode())
                except:
                    continue
        
        client.send("<END>".encode())
        break
    
    return
        
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

        sendHashlist(client)
        
        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()

def messagesTreatment(client):
    while True:
        for path,dirs,files in os.walk('send'):
            for file in files:
                filename = os.path.join(path,file)
                relpath = os.path.relpath(filename,'send')
                filesize = os.path.getsize(filename)

                #print(f'Sending {relpath}')

                with open(filename,'rb') as f:
                    client.sendall(relpath.encode() + b'\n')
                    client.sendall(str(filesize).encode() + b'\n')

                    # Send the file in chunks so large files can be handled.
                    while True:
                        data = f.read(1000000)
                        if not data: break
                        client.sendall(data)           

        break
        
        # try: 
        #     namefile = client.recv(1024).decode()
        #     with open(namefile,'rb') as file:
        #         for data in file.readlines():
        #             client.send(data)

        # except:
        #     print("algo deu errado messagesTreatment")
        #     break

        


main()
