import socket
import time
import json
from threading import Thread

class RegistroUsuario:
    def __init__(self, nome=None, endereco=None, telefone=None, email=""):
        self.dados = {"Nome" : nome,
                      "Endereço": endereco,
                      "Telefone": telefone,
                      "Email" : email}

    def recupera_campos(self):
        return self.dados

    def seta_campo(self, nomeCampo, valor):
        if nomeCampo in self.dados:
            self.dados[nomeCampo] = valor
        else:
            raise Exception(f"Campo {nomeCampo} inexistente")

class ServidorAtendimento:
    def __init__(self, endereco_servidor="0.0.0.0", porta_servidor=3213, max_conexoes=1):
        # Procedimento de criação do socket e configuração
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((endereco_servidor, porta_servidor))
        self.socket.listen(max_conexoes)

        # Registro de thread para atendimento e registros de usuários
        self.threadClientes = {}
        self.registrosDeUsuarios = {}

        # Inicia uma thread dedicada para escuta de novas conexões
        
        self.threadEscuta = Thread(target=self.implementacaoThreadEscuta)
        self.threadEscuta.run()

    def handlerDeMensagem(self, mensagem):
        arquivof = open("ArquivoRecebido.txt",'wb') #abrir o arquivo para escrita
        arquivof.write(mensagem)# escreve no arquivo o buffer recebido
        arquivof.close()
        return mensagem

    def implementacaoThreadCliente(self, enderecoDoCliente, socketParaCliente):
        retries = 3
        socketParaCliente.settimeout(1) # timout de 10 segundos


        while True:
            try:
                mensagem = socketParaCliente.recv(512) # aguarda por comando
            except TimeoutError as e:
                print(f"Cliente {enderecoDoCliente} não enviou mensagens nos últimos 10 minutos. Encerrando a conexão")
                socketParaCliente.close() # fecha a conexão com o cliente pelo lado do servidor
                break # quebra o loop infinito e termina a thread
            except Exception as e:
                # caso o socket tenha a conexão fechada pelo cliente ou algum outro erro que não timeout
                print(f"Cliente {enderecoDoCliente} fechou a conexão com exceção: {e}")
                break

            # Se a mensagem for vazia, espere a próxima
            if len(mensagem) != 0:
                retries = 3
            else:
                retries -= 1
                if retries == 0:
                    break
                continue


            print(f"Servidor recebeu do cliente {enderecoDoCliente} a mensagem: {mensagem.decode}")

            # Decodifica mensagem em bytes para utf-8 e
            # em seguida decodifica a mensagem em Json para um dicionário Python
            mensagem_decodificada = mensagem

            # Por enquanto, retorna a mensagem recebida
            resposta = self.handlerDeMensagem(mensagem_decodificada)

            # fim do whil
            print(f"Servidor enviou para o cliente {enderecoDoCliente} a mensagem: {resposta}")

            socketParaCliente.send(resposta)

        # Testaremos apenas com um usuário por servidor
        # Forçaremos a parada da thread de escuta fechando socket
        self.socket.close()

    def implementacaoThreadEscuta(self):
        while True:
            # Thread fica bloqueada enquanto aguarda por conexões,
            # enquanto servidor continua rodando normalmente
            try:
                (socketParaCliente, enderecoDoCliente) = self.socket.accept()
            except OSError:
                # Como fechamos o socket na thread para cliente,
                # quando tentarmos escutar no mesmo socket, ele não mais
                # existirá e lançará um erro
                # Não é isso que servidores de verdade fazem, é só um exemplo
                time.sleep(1)
                print(f"Servidor: desligando thread de escuta")
                break
            self.threadClientes[enderecoDoCliente] = Thread(target=self.implementacaoThreadCliente,
                                                            args=(enderecoDoCliente, socketParaCliente),
                                                            daemon=True) # thread sem necessidade de join, será morta ao final do processo
            self.threadClientes[enderecoDoCliente].run() # inicia thread de atendimento ao novo cliente conectado



def cliente():
    # Recupera endereço do servidor
    socket_cliente_thread = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    nome_servidor = socket.gethostname()
    ip_servidor = socket.gethostbyname_ex(nome_servidor)
    print(ip_servidor)
    #socket_cliente_thread.bind(ip_servidor[2][1],3213)
    #socket_cliente_thread.listen(10)
    # coloca a thread para dormir por dois segundos enquanto o servidor é iniciado
    # conecta com o servidor

    arquivo = open("ArquivoEnviado.txt","rb")# nome do arqquivo    
    mensagem = arquivo.read(512)
    arquivo.close()
    # Transforma dicionário em JSON e em seguida para bytes
    #mensagem_bytes = json.dumps(mensagem).encode("utf-8")
    #print(mensagem_bytes,"b")
    # envia mensagem ao servidor
    socket_cliente_thread.connect((ip_servidor[2][1], 3213))
    socket_cliente_thread.send(mensagem)
    msg = socket_cliente_thread.recv(512)
    print("Cliente:", msg)
    socket_cliente_thread.close()
    print("Cliente:", socket_cliente_thread)


from concurrent.futures import ThreadPoolExecutor
threadPool = ThreadPoolExecutor()

threadPool.submit(cliente)

# Cria o servidor

servidor = ServidorAtendimento()
del servidor



##############cliente


# while True:
#     sc, address = recebe.accept()

    
#     arquivof = open("recebido_oi.txt",'wb') #abrir o arquivo para escrita
#     fim =0
#     while (fim==0):       
    
#         ler_bfferl = sc.recv(1024) #aloca no buffer o que foi recebido
        
#         while (ler_bfferl):
                
#                 arquivof.write(ler_bfferl)# escreve no arquivo o buffer recebido
#                 ler_bfferl = sc.recv(1024) # aloca o resto no buffer
                
#                 fim=1
                 
#     arquivof.close()


#     sc.close()