import sqlite3
from tkinter import messagebox

class SistemaDeRegistro:
    def __init__(self):
        self.conn = sqlite3.connect('estudante.db')
        self.c = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS estudantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            tel TEXT NOT NULL,
            sexo TEXT,
            data_nascimento TEXT NOT NULL,
            endereco TEXT,
            curso TEXT NOT NULL,
            picture TEXT 
        )''') 
        self.conn.commit()
    
    def register_student(self, student):
        self.c.execute(
            "INSERT INTO estudantes (nome, email, tel, sexo, data_nascimento, endereco, curso, picture) VALUES (?,?,?,?,?,?,?,?)",
            student
        )
        self.conn.commit() 
        messagebox.showinfo('Sucesso', "Registrado com sucesso!")

    def view_all_students(self):
        self.c.execute("SELECT * FROM estudantes")
        dados = self.c.fetchall()
        return dados

    def search_student(self, valor):
        try:
            valor_int = int(valor)
            self.c.execute("SELECT * FROM estudantes WHERE id=?", (valor_int,))
            dados = self.c.fetchone()
        except ValueError:
            # Busca por nome
            self.c.execute("SELECT * FROM estudantes WHERE nome LIKE ?", ('%' + valor + '%',))
            dados = self.c.fetchone()
        return dados

    def update_student(self, novos_valores):
        query = "UPDATE estudantes SET nome=?, email=?, tel=?, sexo=?, data_nascimento=?, endereco=?, curso=?, picture=? WHERE id=?"
        self.c.execute(query, novos_valores)
        self.conn.commit()
        messagebox.showinfo('Sucesso', f'Estudante com ID {novos_valores[-1]} foi atualizado!')

    def delete_student(self, id):
        self.c.execute("DELETE FROM estudantes WHERE id=?", (id,))
        self.conn.commit()
        messagebox.showinfo('Sucesso', f'Estudante com ID {id} foi deletado!')
        
    def close_connection(self):
        self.conn.close()