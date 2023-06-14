from tkinter import *
from tkinter import Tk, ttk, messagebox

usuarios = ['joao', '12345']
files = ["file1", "file2", "file3"]

def verifica_senha():
    user = e_user.get()
    senha = e_pw.get()

    if usuarios[0] == user and usuarios[1] == senha:
        janela.destroy()
        global main
        main = Tk()
        main.title("Main")
        main.geometry("450x400")
        main.configure(background=c1)
        main.resizable(width=FALSE, height=FALSE)
        b_send = Button(main, command=send, text='Enviar', width=20, height=2, font=('Ivy 8 bold'), relief=RAISED, overrelief=RIDGE)
        b_send.place(x=40, y=180)
        b_receive = Button(main, command=receive, text='Receber', width=20, height=2, font=('Ivy 8 bold'), relief=RAISED, overrelief=RIDGE)
        b_receive.place(x=250, y=180)
        
    else:
        messagebox.showwarning('Erro', 'Verifique nome e sennha')

def send():
    main.destroy()
    send = Tk()
    send.title("Enviar")
    send.geometry("450x400")
    send.configure(background=c1)
    send.resizable(width=FALSE, height=FALSE)
    l_key = Label(send, text='Chave', anchor=NW, font=('Ivy 25'), bg=c1, fg=c4)
    l_key.place(x=15, y=100)
    e_key = Entry(send, width=25, justify='left', font=("", 15), highlightthickness=1, relief='solid')
    e_key.place(x=14, y=150)

def receive():
    main.destroy()
    receive = Tk()
    receive.title("Receber")
    receive.geometry("450x400")
    receive.configure(background=c1)
    receive.resizable(width=FALSE, height=FALSE)
    l_key = Label(receive, text='Chave', anchor=NW, font=('Ivy 25'), bg=c1, fg=c4)
    l_key.place(x=15, y=40)
    e_key = Entry(receive, width=25, justify='left', font=("", 15), highlightthickness=1, relief='solid')
    e_key.place(x=14, y=80)
    l_files = Label(receive, text='Lista de arquivos', anchor=NW, font=('Ivy 25'), bg=c1, fg=c4)
    l_files.place(x=15, y=130)
    c_files = ttk.Combobox(receive, values=files, width=25)
    c_files.place(x=15, y=170)


#cores
c0 = "#f0f3f5" # preto
c1 = "#feffff" #  branco
c2 = "#3fb5a3" # verde
c3 = "#38576b" # valor
c4 = "#403d3d" # letra

# criacao da janela
janela = Tk()
janela.title ("Login")
janela.geometry("450x400")
janela.configure(background=c1)
janela.resizable(width=FALSE, height=FALSE)

#divisao da janela
frame_cima = Frame(janela, width=450, height=55, bg=c1, relief='flat')
frame_cima.grid(row=0, column=0, pady=1, padx=0, sticky=NSEW)

frame_baixo = Frame(janela, width=450, height=250, bg=c1, relief='flat')
frame_baixo.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

# config frame cima
l_nome = Label(frame_cima, text='Login', anchor=NE, font=('Ivy 35'), bg=c1, fg=c4)
l_nome.place(x=5, y=5)

l_linha = Label(frame_cima, text='', width=350, anchor=NW, font=('Ivy 35'), bg=c2, fg=c4)
l_linha.place(x=10, y=50)

# config frame baixo
l_user = Label(frame_baixo, text='Usuário', anchor=NW, font=('Ivy 25'), bg=c1, fg=c4)
l_user.place(x=15, y=20)
e_user = Entry(frame_baixo, width=25, justify='left', font=("", 15), highlightthickness=1, relief='solid')
e_user.place(x=14, y=55)

l_pw = Label(frame_baixo, text='Senha', anchor=NW, font=('Ivy 25'), bg=c1, fg=c4)
l_pw.place(x=15, y=95)
e_pw = Entry(frame_baixo, width=25, justify='left', font=("", 15), highlightthickness=1, relief='solid')
e_pw.place(x=14, y=130)

b_login = Button(frame_baixo, command=verifica_senha, text='Entrar', width=40, height=2, font=('Ivy 8 bold'), relief=RAISED, overrelief=RIDGE)
b_login.place(x=15, y=180)


janela.mainloop()