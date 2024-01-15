import re
from tkinter import messagebox
import mysql.connector
from tkinter import *
from tkinter import ttk
import xlsxwriter
from tkinter import Tk, Toplevel
import reportlab
from reportlab.pdfgen import canvas



def conecta_banco():
    sql = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database= 'loja'
    )
    return sql


sql = mysql.connector.connect(
  host='127.0.0.1',
  user='root',
  password=''
)

dados = sql.cursor()
dados.execute('SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = "loja";')
resultado = dados.fetchone()[0]

if resultado > 0 :
    sql.close()
    sql = conecta_banco()

else:
    
    dados.execute('CREATE DATABASE loja;')
    sql.commit()
    
    sql = conecta_banco()

    dados = sql.cursor()
    dados.execute('CREATE TABLE funcionarios (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), telefone VARCHAR(255),vendas VARCHAR(255), email VARCHAR(255));')
    dados.execute('CREATE TABLE eletronicos (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), quantidade VARCHAR(255),valor VARCHAR(255));')

    sql.commit()
    sql.close()



class app_loja():
    
    def __init__(self,window):
        
        
        
        
        
        self.sql = conecta_banco()
        self.dados = self.sql.cursor()
        
        
        
        
        
        self.window = window
        self.window.title('Banco de dados da loja')

        self.table = ttk.Treeview(self.window, columns=('ID', 'Nome', 'Telefone','Vendas','Email'), show='headings')
        self.table.heading('ID', text='ID')
        self.table.heading('Nome', text='Nome')
        self.table.heading('Telefone', text='Telefone')
        self.table.heading('Vendas', text='Vendas')
        self.table.heading('Email', text='Email')
        self.table.pack(fill=BOTH, expand=True)

        self.add_btn = Button(self.window, text='Adicionar funcionario',command=self.add_data_window)
        
        self.update_button = Button(self.window, text='Atualizar',command=self.atualiza_dados_window)
        
        self.delete_button = Button(self.window, text='Deletar',command=self.deleta_funcionario)
        
        self.buttons = [self.add_btn,self.update_button,self.delete_button]
        self.alinha_btn_esquerda()

        
        self.fetch_data()
        

    def alinha_btn_esquerda(self):
        for button in self.buttons:
            
            button.pack(side=LEFT) 

    def add_data_window(self):
        # Janela para adicionar dados
        # Cria uma nova janela chamada add_window como filha da janela principal
        # Configura a nova janela para que sua origem esteja no canto superior esquerdo da janela principal
        add_window = Toplevel(self.window)
        add_window.title('Adicionar funcionario')

        # Entradas para adicionar dados
        nome_label = Label(add_window, text='Nome:')
        nome_label.grid(row=0, column=0, padx=10, pady=10)
        nome_entry = Entry(add_window)
        nome_entry.grid(row=0, column=1, padx=10, pady=10)

        telefone_label = Label(add_window, text='Telefone:')
        telefone_label.grid(row=1, column=0, padx=10, pady=10)
        telefone_entry = Entry(add_window)
        telefone_entry.grid(row=1, column=1, padx=10, pady=10)
    
        vendas_label = Label(add_window, text='Vendas:')
        vendas_label.grid(row=2, column=0, padx=10, pady=10)
        vendas_entry = Entry(add_window)
        vendas_entry.grid(row=2, column=1, padx=10, pady=10)
        
        email_label = Label(add_window, text='Email:')
        email_label.grid(row=3, column=0, padx=10, pady=10)
        email_entry = Entry(add_window)
        email_entry.grid(row=3, column=1, padx=10, pady=10)

        # Botão para confirmar a adição
        confirm_btn = Button(add_window, text='Adicionar', command=lambda: self.add_data(nome_entry.get(), telefone_entry.get(),vendas_entry.get() ,email_entry.get(), add_window))
        confirm_btn.grid(row=4, column=0, columnspan=2, pady=10)


    def add_data(self, nome, telefone, vendas,email, add_window):
        if nome == '' or telefone == '' or email == '':
            messagebox.showerror('Erro', 'Todos os campos devem ser preenchidos.')
            return False

        if not re.match(r'^[0-9]+$', telefone):
            messagebox.showerror('Erro', 'O número de telefone deve conter apenas números.')
            return False

        if '@' not in email:
            messagebox.showerror('Erro', 'O e-mail deve conter um @.')
            return False
        
        if not re.match(r'^[0-9]+$', vendas):
            messagebox.showerror('Erro', 'O número de vendas deve conter apenas números.')
            return False
        
        self.dados.execute('INSERT INTO funcionarios (nome, telefone, vendas, email) VALUES (%s, %s, %s ,%s)', (nome, telefone, vendas,email))
        self.sql.commit()
        add_window.destroy()
        self.fetch_data()
        
    def fetch_data(self):
        # Buscar dados do banco de dados e popular a tabela treeview
        
        self.dados.execute('SELECT * FROM funcionarios')
        rows = self.dados.fetchall()

        # Limpar dados anteriores
        for row in self.table.get_children():
            self.table.delete(row)

        # Adicionar novos dados
        for row in rows:
            self.table.insert('', 'end', values=row)

        # Adicionar um evento de seleção
        self.table.bind('<<TreeviewSelect>>', self.on_select)
        
        
    def on_select(self, event):
        # Obter o item selecionado
        item = self.table.selection()[0]

        # Pegar os dados do item selecionado
        data = self.table.item(item, 'values')
        id = data[0]
        nome = data[1]
        telefone = data[2]
        vendas = data[3]
        email = data[4]
        
        
    def atualiza_dados_window(self):
    
        if self.table.selection():
            # Janela para atualizar dados
            update_window = Toplevel(self.window)
            update_window.title('Atualizar Contato')

            nome_label = Label(update_window, text='Nome:')
            nome_label.grid(row=0, column=0, padx=10, pady=10)
            nome_entry = Entry(update_window)
            nome_entry.grid(row=0, column=1, padx=10, pady=10)

            telefone_label = Label(update_window, text='Telefone:')
            telefone_label.grid(row=1, column=0, padx=10, pady=10)
            telefone_entry = Entry(update_window)
            telefone_entry.grid(row=1, column=1, padx=10, pady=10)
        
            vendas_label = Label(update_window, text='Vendas:')
            vendas_label.grid(row=2, column=0, padx=10, pady=10)
            vendas_entry = Entry(update_window)
            vendas_entry.grid(row=2, column=1, padx=10, pady=10)
            
            email_label = Label(update_window, text='Email:')
            email_label.grid(row=3, column=0, padx=10, pady=10)
            email_entry = Entry(update_window)
            email_entry.grid(row=3, column=1, padx=10, pady=10)

            confirm_btn = Button(update_window, text='Atualizar', command=lambda: self.update_data(nome_entry.get(), telefone_entry.get(),vendas_entry.get() ,email_entry.get(), update_window))
            confirm_btn.grid(row=4, column=0, columnspan=2, pady=10)
        else:
            
            messagebox.showerror('Erro', 'Nenhum registro selecionado.')
    
        
    def update_data(self,nome, telefone, vendas,email,update_window):
    
        item = self.table.selection()[0]
        data = self.table.item(item, 'values')
        id = data[0]
        # Atualizar dados no banco de dados
        # o objeto 'cursor' é utilizado para executar a instrução SQL
        
        self.dados.execute('UPDATE funcionarios SET nome=%s, telefone=%s,vendas=%s, email=%s WHERE id=%s', (nome, telefone, vendas,email,id))
        # Confirma a alteração no banco de dados usando a função commit
        self.sql.commit()
        # Fecha a janela de atualização
        update_window.destroy()
        # Recupera os dados atualizados da tabela 'contatos' usando a função 'fetch_data'
        self.fetch_data()
    
    
        
    def deleta_funcionario(self):
        
        if self.table.selection():
            item = self.table.selection()[0]
                
            data = self.table.item(item, 'values')
            id = data[0]

            
            if messagebox.askyesno('Confirmação', 'Tem certeza de que deseja excluir o registro?'):

                self.dados.execute(f'DELETE FROM funcionarios WHERE id={id}')
                self.sql.commit()
                self.fetch_data()
        
        else:
            messagebox.showerror('Erro', 'Nenhum registro selecionado.')
        
        
        
if __name__ == '__main__':
    window = Tk()
    app = app_loja(window)
    window.mainloop()
    