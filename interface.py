from tkinter import *

from tkinter.ttk import Style
from tkinter import messagebox, filedialog as fd
from PIL import ImageTk, Image
from tkcalendar import Calendar, DateEntry
from datetime import date
from tkinter import ttk
import shutil
import os


#importando main 
from main import SistemaDeRegistro  
sistema_de_registro = SistemaDeRegistro()  

# cores
co0 = "#2e2d2b"  
co1 = "#feffff"     
co2 = "#e5e5e593"  
co3 = "#00a095"  
co4 = "#403d3d"  
co6 = "#DA98CC"  
co7 = "#ef5350"  
co8 = "#7E09C7"  
co9 = "#e9edf5"  

# criando janela
janela = Tk()
janela.title("")
janela.geometry("1050x550") 
janela.configure(background=co1) 
janela.resizable(width=FALSE, height=FALSE)
style = Style(janela)
style.theme_use("clam")

#ESTILO DA TABELA 
style.configure("Treeview",
    background="#EEEEEE",    #fundo da tabela
    foreground="black",      #texto
    rowheight=25,            # altura das linhas
    fieldbackground="#EEEEEE"  # fundo das células
)

style.map("Treeview", background=[("selected", "#DA98CC")])  # cor ao selecionar linha


# criando frames
frame_logo = Frame(janela, width=850, height=52, bg=co6)
frame_logo.grid(row=0, column=0, pady=0, padx=0, sticky=NSEW, columnspan=5)

#parte dos botões
frame_botoes = Frame(janela, width=300, height=200, bg=co1, relief=RAISED)
frame_botoes.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)
frame_details = Frame(janela, width=800, height=100, bg=co1, relief=SOLID)
frame_details.grid(row=1, column=1, pady=1, padx=10, sticky=NSEW)
frame_tabela = Frame(janela, width=800, height=100, bg=co1, relief=SOLID)
frame_tabela.grid(row=3, column=0, pady=0, padx=10, sticky=NSEW, columnspan=5)

#trabalhando no frame do logo
global imagem, imagem_string, I_imagem
app_lg = Image.open('imagens/chapeu.png')
app_lg.thumbnail((50,50))
app_lg = ImageTk.PhotoImage(app_lg)
app_logo = Label(frame_logo, image=app_lg, text="FAMEL", width=850, compound=LEFT, anchor=NW, font=('Arial', 15, 'bold'), bg= co6, fg= co1) 
app_logo.place(x=5, y=0)

#criando funções para GRID
#função adicionar
def adicionar():
    global imagem, imagem_string, I_imagem
    # obtendo valores
    nome = e_nome.get()
    email = e_email.get()  
    tel = e_tel.get()
    sexo = c_sexo.get()
    data = nascimento.get()  
    endereço = e_endereço.get()
    curso = c_curso.get()
    img = imagem_string
    lista = [nome, email, tel, sexo, data, endereço, curso, img]

    
    for i in lista:
        if i == '':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return
    # registrando os valores
    sistema_de_registro.register_student(lista)
    # limpando os campos de entrada
    e_nome.delete(0, END)
    e_email.delete(0, END)
    e_tel.delete(0, END)
    c_sexo.delete(0, END)
    nascimento.delete(0, END)
    e_endereço.delete(0, END)
    c_curso.delete(0, END)
    #abrindo imagem
    img = Image.open("imagens/chapeu.png")
    img = img.resize((100, 100))
    img_tk = ImageTk.PhotoImage(img)
    I_imagem = Label(frame_details, image=img_tk, bg=co1, fg=co4)
    I_imagem.place(x=390, y=10)
    # mostrando os valores na tabela
    mostrar_alunos()
    
#função procurar
def procurar():
    global imagem, imagem_string, I_imagem
    valor = e_procurar.get().strip()

    if not valor:
        messagebox.showerror("Erro", "Digite o ID ou nome do aluno")
        return

    dados = sistema_de_registro.search_student(valor)

    if not dados:
        messagebox.showinfo("Aviso", "Aluno não encontrado")
        return

    e_procurar.delete(0, END)
    e_procurar.insert(END, dados[0])

    e_nome.delete(0, END)
    e_email.delete(0, END)
    e_tel.delete(0, END)
    c_sexo.set('')
    nascimento.set_date(date.today())
    e_endereço.delete(0, END)
    c_curso.set('')

    e_nome.insert(END, dados[1])
    e_email.insert(END, dados[2])
    e_tel.insert(END, dados[3])
    c_sexo.set(dados[4])
    
    try:
        data_obj = date.fromisoformat(dados[5])
        nascimento.set_date(data_obj)
    except ValueError:
        pass

    e_endereço.insert(END, dados[6])
    c_curso.set(dados[7])

    imagem = dados[8]
    global imagem_string
    imagem_string = imagem

    if imagem and imagem != '':
        try:
            img = Image.open(imagem)
            img = img.resize((130, 130))
            img_tk = ImageTk.PhotoImage(img)
            I_imagem.config(image=img_tk)
            I_imagem.image = img_tk
        except Exception:
            img = Image.open("imagens/chapeu.png")
            img = img.resize((130, 130))
            img_tk = ImageTk.PhotoImage(img)
            I_imagem.config(image=img_tk)
            I_imagem.image = img_tk
    else:
        img = Image.open("imagens/chapeu.png")
        img = img.resize((130, 130))
        img_tk = ImageTk.PhotoImage(img)
        I_imagem.config(image=img_tk)
        I_imagem.image = img_tk


#Função atualizar
def atualizar():
    global imagem, imagem_string, I_imagem
    id_aluno = int(e_procurar.get())
    nome = e_nome.get()
    email = e_email.get()
    tel = e_tel.get()
    sexo = c_sexo.get()
    data_nasc = nascimento.get()
    endereço = e_endereço.get()
    curso = c_curso.get()
    lista = [nome, email, tel, sexo, data_nasc, endereço, curso, imagem_string, id_aluno]
    sistema_de_registro.update_student(lista)
    mostrar_alunos()
    messagebox.showinfo('Sucesso', 'Dados atualizados com sucesso!')
    dados = sistema_de_registro.search_student(id_aluno)
    e_nome.delete(0, END)
    e_email.delete(0, END)
    e_tel.delete(0, END)
    c_sexo.delete(0, END)
    nascimento.delete(0, END)
    e_endereço.delete(0, END)
    c_curso.delete(0, END)
    e_nome.insert(END, dados[1])
    e_email.insert(0, dados[2])
    e_tel.insert(0, dados[3])
    c_sexo.insert(0, dados[4])
    nascimento.insert(0, dados[5])
    e_endereço.insert(0, dados[6])
    c_curso.insert(0, dados[7])
    img = Image.open("imagens/chapeu.png")
    img = img.resize((130, 130))
    img_tk = ImageTk.PhotoImage(img)
    imagem = dados[8]
    imagem_string = imagem
    I_imagem = Label(frame_details, image=img_tk, bg=co1, fg=co4)
    I_imagem.place(x=390, y=10)
    img = Image.open("imagens/chapeu.png")
    img = img.resize((130, 130))
    img_tk = ImageTk.PhotoImage(img)
    I_imagem.config(image=img_tk)
    I_imagem.image = img_tk

#função deletar 
def deletar():
    try:
        id_aluno = int(e_procurar.get())

        resposta = messagebox.askyesno("Confirmar", f"Tem certeza que deseja deletar o aluno com ID {id_aluno}?")
        if resposta:
            sistema_de_registro.delete_student(id_aluno)
            messagebox.showinfo("Sucesso", f"Aluno com ID {id_aluno} deletado com sucesso.")
            mostrar_alunos()
            # Limpa os campos
            e_nome.delete(0, END)
            e_email.delete(0, END)
            e_tel.delete(0, END)
            c_sexo.set('')
            nascimento.set_date(date.today())
            e_endereço.delete(0, END)
            c_curso.set('')
            e_procurar.delete(0, END)
            # Reseta a imagem
            img = Image.open("imagens/chapeu.png")
            img = img.resize((130, 130))
            img_tk = ImageTk.PhotoImage(img)
            I_imagem.config(image=img_tk)
            I_imagem.image = img_tk
    except ValueError:
        messagebox.showerror("Erro", "Digite um ID válido.")

#abrindo imagem
img = Image.open("imagens/chapeu.png")
img = img.resize((130, 130))
img_tk = ImageTk.PhotoImage(img)
I_imagem = Label(frame_details, image=img_tk, bg=co1, fg=co4)
I_imagem.place(x=390, y=10)
#criando os campos de entrada
i_nome = Label(frame_details, text= "Nome", anchor = NW, font=('Ivy 10'), bg=co1, fg=co4)
i_nome.place(x=4, y=10)
e_nome = Entry(frame_details, width=30, justify='left', relief='solid')
e_nome.place(x=7,y=40)
i_email = Label(frame_details, text="email", anchor = NW, font=('Ivy 10'), bg=co1, fg=co4)
i_email.place(x=4, y=70)
e_email = Entry(frame_details, width=30, justify='left', relief='solid')
e_email.place(x=7,y=100)
i_tel = Label(frame_details, text="Telefone", anchor = NW, font=('Ivy 10'), bg=co1, fg=co4)
i_tel.place(x=4, y=130)
e_tel = Entry(frame_details, width=15, justify='left', relief='solid')
e_tel.place(x=7,y=160)
sexo = Label(frame_details, text="Sexo", anchor = NW, font=('Ivy 10'), bg=co1, fg=co4)
sexo.place(x=124, y=130)
c_sexo = ttk.Combobox(frame_details, width=7, font= ('Ivy 8 bold'), justify= 'center')
c_sexo["values"] = ("M", "F", "I")
c_sexo.place(x=130, y=160)
i_nascimento = Label(frame_details, text="Data de nascimento", anchor = NW, font=('Ivy 10'), bg=co1, fg=co4)
i_nascimento.place(x=220, y=10)
nascimento = DateEntry (frame_details, width=18, justify="center", background= "darkblue", foreground = "white", borderwidth=2, year=2025)
nascimento.place(x=224, y=40)
i_endereço = Label(frame_details, text="Endereço", anchor = NW, font=('Ivy 10'), bg=co1, fg=co4)
i_endereço.place(x=220, y=70)
e_endereço = Entry(frame_details, width=15, justify='left', relief='solid')
e_endereço.place(x=224,y=100)
cursos = 'Medicina', 'Direito', 'História', 'Ciências contábeis', 'Psicologia', "Enfermagem", "Matemática"   
curso = Label(frame_details, text="Curso", anchor = NW, font=('Ivy 10'), bg=co1, fg=co4)
curso.place(x= 220, y=130)
c_curso = ttk.Combobox(frame_details, width=20, font= ('Ivy 8 bold'), justify= 'center')
c_curso["values"] = (cursos)
c_curso.place(x=220, y=160)

#Função para escolher imagem
def escolher_imagem():
    caminho_original = fd.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    if caminho_original:
        nome_aluno = e_nome.get().strip().replace(" ", "_")
        if not nome_aluno:
            messagebox.showerror("Erro", "Digite o nome do aluno antes de carregar a imagem.")
            return

        nome_arquivo = f"{nome_aluno}.jpg"
        destino = os.path.join("imagens", nome_arquivo)

        try:
            shutil.copy(caminho_original, destino)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao copiar imagem: {e}")
            return

        img = Image.open(destino)
        img = img.resize((130, 130))
        img_tk = ImageTk.PhotoImage(img)
        I_imagem.config(image=img_tk)
        I_imagem.image = img_tk

        global imagem_string
        imagem_string = destino

# tabela de alunos
def mostrar_alunos():
    list_header = ['id', 'nome', "email", "telefone", "sexo", "nascimento", "endereço", "curso"]
    df_list = sistema_de_registro.view_all_students()
    global tree_aluno
    tree_aluno = ttk.Treeview(frame_tabela, selectmode="extended", columns=list_header, show="headings")
    #vertical 
    vsb = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree_aluno.yview)
    #horizontal
    hsb = ttk.Scrollbar(frame_tabela, orient="horizontal", command=tree_aluno.xview)
    tree_aluno.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree_aluno.grid(column=0, row=0, sticky="nsew")
    
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')
    frame_tabela.grid_rowconfigure(0, weight=12)   
    frame_tabela.grid_columnconfigure(0, weight=1)
    hd = ["center", "center", "center", "center", "center", "center", "center", "center"]
    h = [2, 100, 180, 80, 10, 80, 70, 20]
    n = 0
    for col in list_header:
        tree_aluno.heading(col, text=col.title(), anchor=NW)
        tree_aluno.column(col, width=h[n], anchor=hd[n])
        n += 1
    for item in df_list:
        tree_aluno.insert('', 'end', values=item)
        
#procurar aluno
frame_procurar = Frame(frame_botoes, width=40, height=52, bg=co1, relief=RAISED)
frame_procurar.grid(row=0, column=0, pady=10, padx=10, sticky=NSEW)
i_nome = Label(frame_procurar, text="Procurar[Extra ID]", anchor = NW, font=('Ivy 10'), bg=co1, fg=co4)
i_nome.grid(row=0, column=0, pady=10, padx=0, sticky=NSEW)

e_procurar = Entry(frame_procurar, width=20, justify='center', relief='solid', font=("Ivy 10"))
e_procurar.grid(row=0, column=0, padx=(0, 5), pady=10)

botao_alterar = Button(frame_procurar, command=procurar, text="Procurar", width=10, anchor=CENTER, overrelief=RIDGE, font=('Ivy 7 bold'), bg=co1, fg=co0)
botao_alterar.grid(row=0, column=1, pady=10)


#botoes
app_img_adicionar = Image.open('imagens/adicionar.png')
app_img_adicionar= app_img_adicionar.resize((25,25))
app_img_adicionar= ImageTk.PhotoImage(app_img_adicionar)
app_adicionar = Button(frame_botoes, command= adicionar, image=app_img_adicionar, relief= GROOVE, text="Adicionar", width=200, compound=LEFT, anchor=CENTER, overrelief=RIDGE, font=('Ivy 11'), bg=co1, fg=co0)
app_adicionar.grid (row=1, column=0, pady=5, padx=10, sticky=NSEW)

app_img_atualizar = Image.open('imagens/atualizar.png')
app_img_atualizar = app_img_atualizar.resize((25,25))
app_img_atualizar = ImageTk.PhotoImage(app_img_atualizar)
app_atualizar = Button(frame_botoes, command=atualizar, image=app_img_atualizar, relief=GROOVE, text="Atualizar", width=100, compound=LEFT, anchor=CENTER, overrelief=RIDGE, font=('Ivy 11'), bg=co1, fg=co0)
app_atualizar.grid (row=2, column=0, pady=5, padx=10, sticky=NSEW)

app_img_deletar = Image.open('imagens/deletar.png')
app_img_deletar = app_img_deletar.resize((27,25))
app_img_deletar = ImageTk.PhotoImage(app_img_deletar)
app_deletar = Button(frame_botoes, command=deletar, image=app_img_deletar, relief= GROOVE, text="Deletar", width=100, compound=LEFT, anchor=CENTER, overrelief=RIDGE, font=('Ivy 11'), bg=co1, fg=co0)

# Botão para carregar imagem
botao_carregar_imagem = Button(frame_details, text="Carregar Foto",command=escolher_imagem, width=15, overrelief=RIDGE, font=('Ivy 9 bold'), bg=co6, fg=co1)
botao_carregar_imagem.place(x=400, y=150)


app_deletar.grid (row=3, column=0, pady=5, padx=10, sticky=NSEW)

#linha separatória
l_linha = Label(frame_botoes, relief= GROOVE, width=1, height=123, anchor=NW, font=('Ivy 1'), bg=co1, fg=co1)
l_linha.place(x=230, y=15)
#chamar a tabela
mostrar_alunos()
janela.mainloop()
