from tkinter import *
from tkinter import Tk, ttk

#cores
c0 = "#f0f3f5" # preto
c1 = "#feffff" #  branco
c2 = "#3fb5a3" # verde
c3 = "#38576b" # valor
c4 = "#403d3d" # letra

# criacao da janela
janela = Tk()
janela.title ("Peer to Peer")
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

b_login = Button(frame_baixo, text='Entrar', width=40, height=2, font=('Ivy 8 bold'), relief=RAISED, overrelief=RIDGE)
b_login.place(x=15, y=180)




janela.mainloop()