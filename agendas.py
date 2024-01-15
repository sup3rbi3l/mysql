import re
from tkinter import messagebox
import mysql.connector
from tkinter import *
from tkinter import ttk
import xlsxwriter
from tkinter import Tk, Toplevel
import reportlab
from reportlab.pdfgen import canvas

# Conectar ao banco de dados MySQL
cnx = mysql.connector.connect(
  host='127.0.0.1',
  user='root',
  password=''
)

# Executar a instrução SQL para verificar se o banco de dados existe
cursor = cnx.cursor()
cursor.execute('SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = "agenda";')

# Obter o número de resultados
num_results = cursor.fetchone()[0]

# Fechar a conexão com o banco de dados
cnx.close()

# Se o número de resultados for maior que zero, o banco de dados existe
if num_results > 0:
  print('O banco de dados agenda existe e esta pronto para uso.')
else:
    # Conectar-se ao servidor MySQL para criar o banco de dados
    cnx = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password=''
    )

    # Criar o banco de dados agenda
    cursor = cnx.cursor()
    cursor.execute('CREATE DATABASE agenda;')
    cnx.commit()

    # Conectar-se ao banco de dados agenda recém-criado
    cnx = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='agenda'  # Especificar o banco de dados
    )

    # Criar a tabela contatos
    cursor = cnx.cursor()
    cursor.execute('CREATE TABLE contatos (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), telefone VARCHAR(255), email VARCHAR(255));')
   
    cursor.execute("""
    CREATE TABLE grupos (
      id INT AUTO_INCREMENT PRIMARY KEY,
      nome VARCHAR(255)
    )
  """)
  
    # Fechar a conexão com o banco de dados
    cnx.commit()
    cnx.close()
    
 
 

 


# Fechar a conexão com o banco de dados

class CrudApp:

    def __init__(self, window):
        self.window = window
        self.window.title('CRUD usando Python e MySQL')
       

        # Conectar ao banco de dados MySQL
        self.db = mysql.connector.connect(
           # host='localhost',
           host='127.0.0.1',
            user='root',
            password='',
            database='agenda'
        )
       
        # Criar a tabela treeview
        # As colunas da tabela são definidas usando o argumento columns no construtor
        self.table = ttk.Treeview(self.window, columns=('ID', 'Nome', 'Telefone', 'Email'), show='headings')
        # Definindo o cabeçalho das colunas
        # O cabeçalho de cada coluna é definido usando o método heading
        self.table.heading('ID', text='ID')
        self.table.heading('Nome', text='Nome')
        self.table.heading('Telefone', text='Telefone')
        self.table.heading('Email', text='Email')
        # Adicionando a tabela na janela
        # a tabela é adicionada na janela do aplicativo usando o método pack. O argumento fill=BOTH faz com que a tabela ocupe todo o espaço disponível na janela, tanto horizontal quanto verticalmente. O argumento expand=True permite que a tabela seja redimensionada, se necessário
        self.table.pack(fill=BOTH, expand=True)

        # Botão para adicionar
        self.add_btn = Button(self.window, text='Adicionar Contato', command=self.add_data_window)
        self.add_btn.pack()

        # Botões para atualizar e deletar
        self.update_btn = Button(self.window, text='Atualizar', command=self.update_data_window)
        self.update_btn.pack()

        self.delete_btn = Button(self.window, text='Deletar', command=self.delete_data)
        self.delete_btn.pack()

        report_btn = Button(self.window, text='Gerar relatório', command=self.gerar_relatorio)
        report_btn.pack()
        
        self.add_grupo_btn = Button(self.window, text='Adicionar Grupo', command=self.add_data_grupo_window)
        self.add_grupo_btn.pack()
        
        # Botão para limpar dados
        self.clear_data_btn = Button(self.window, text='Limpar Dados', command=self.clear_data_window)
        self.clear_data_btn.pack()
        
        # Botão de excluir banco de dados
        self.deletar_banco_de_dados = Button(self.window, text='Deleta o Banco', command=self.deletar_banco)
        self.deletar_banco_de_dados.pack()
        # Alinhar os botões a esquerda
        self.buttons = [self.add_btn, self.update_btn, self.delete_btn,report_btn, self.add_grupo_btn,self.clear_data_btn]
        self.align_buttons()
        
        # Alinhar os botões a direita
        self.buttons = []
        self.align_buttons_right()
        
        # Atualizar a tabela inicialmente
        self.fetch_data()
    
    def clear_data_window(self):
    # Janela para limpar dados
     self.table.delete(*self.table.get_children())
    # Executar a instrução SQL para excluir todos os registros da tabela contatos
     cursor = self.db.cursor()
    # cursor.execute('DELETE FROM contatos')
    # cursor.execute('DELETE FROM grupos')    
    # cursor.execute("ALTER TABLE contatos DROP COLUMN nome,DROP COLUMN email,DROP COLUMN telefone;") 
     #cursor.execute("ALTER TABLE contato DROP COLUM id and DROP COLUMN nome") 
     cursor.execute("DROP TABLE contatos")
     cursor.execute("DROP TABLE grupos")
     self.db.commit()
     
     
    def deletar_banco(self):
     if messagebox.askyesno('Confirmação', 'Tem certeza de que deseja excluir o banco de dados agenda?'):
    
     
      try:
        cnx = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password=""
        )

        with cnx.cursor() as cursor:
           
            cursor.execute("DROP DATABASE agenda")

        cnx.commit()
       
      except mysql.connector.Error as e:
        print(e)
        messagebox.showerror("Erro", "Falha ao excluir o banco de dados.")
        return

       
        

           
      
           
       
     
    def align_buttons_right(self):
        for button in self.buttons:
            button.pack(side=RIGHT) 
        # Posicionar os botões na horizontal
    
    def align_buttons(self):
        for button in self.buttons:
            button.pack(side=LEFT) 
        # Posicionar os botões na horizontal
           
    def generate_report(self):
     # Obter os dados da tabela
        
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM contatos')
        data = []
        for row in cursor.fetchall():
            data.append(row)

        # Criar um objeto de planilha do Excel
        workbook = xlsxwriter.Workbook('contatos.xlsx')
        worksheet = workbook.add_worksheet()

        # Definir o cabeçalho da planilha
        worksheet.write('A1', 'ID')
        worksheet.write('B1', 'Nome')
        worksheet.write('C1', 'Telefone')
        worksheet.write('D1', 'Email')

        # Escrever os dados da tabela na planilha
        for i, row in enumerate(data):
            worksheet.write(i + 1, 0, row[0])
            worksheet.write(i + 1, 1, row[1])
            worksheet.write(i + 1, 2, row[2])
            worksheet.write(i + 1, 3, row[3])

        # Salvar a planilha
        workbook.close()

        # Exibir uma mensagem de confirmação
        messagebox.showinfo('Sucesso', 'Relatório gerado com sucesso!')
    def gerar_relatorio(self):
        # Obter os dados da tabela
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM contatos')
        data = []
        for row in cursor.fetchall():
            data.append(row)

        # Criar um objeto de relatório PDF
        c = canvas.Canvas('contatos.pdf')

        # Definir o título do relatório
        c.setTitle('Relatório de Contatos')

        # Definir o cabeçalho do relatório
        c.setFont('Times-Roman', 12)
        c.drawString(25, 75, 'Relatório de Contatos')

        # Definir as colunas do relatório
        c.setFont('Times-Roman', 10)
        c.drawString(25, 100, 'ID')
        c.drawString(100, 100, 'Nome')
        c.drawString(200, 100, 'Telefone')
        c.drawString(300, 100, 'Email')
        

        # Escrever os dados da tabela no relatório
        for i, row in enumerate(data):
            c.setFont('Times-Roman', 8)
            c.drawString(25, 125 + i * 25, str(row[0]))
            c.drawString(100, 125 + i * 25, str(row[1]))
            c.drawString(200, 125 + i * 25, str(row[2]))
            c.drawString(300, 125 + i * 25, str(row[3]))

        # Salvar o relatório
        c.save()

        # Exibir uma mensagem de confirmação
        messagebox.showinfo('Sucesso', 'Relatório gerado com sucesso!')

    
    
    
    
    
    
    
    def fetch_data(self):
        # Buscar dados do banco de dados e popular a tabela treeview
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM contatos')
        rows = cursor.fetchall()

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
        email = data[3]
        # Fazer algo com os dados
        
        

    def add_data_window(self):
        # Janela para adicionar dados
        # Cria uma nova janela chamada add_window como filha da janela principal
        # Configura a nova janela para que sua origem esteja no canto superior esquerdo da janela principal
        add_window = Toplevel(self.window)
        add_window.title('Adicionar Contato')

        # Entradas para adicionar dados
        nome_label = Label(add_window, text='Nome:')
        nome_label.grid(row=0, column=0, padx=10, pady=10)
        nome_entry = Entry(add_window)
        nome_entry.grid(row=0, column=1, padx=10, pady=10)

        telefone_label = Label(add_window, text='Telefone:')
        telefone_label.grid(row=1, column=0, padx=10, pady=10)
        telefone_entry = Entry(add_window)
        telefone_entry.grid(row=1, column=1, padx=10, pady=10)
        
        
        

        email_label = Label(add_window, text='Email:')
        email_label.grid(row=2, column=0, padx=10, pady=10)
        email_entry = Entry(add_window)
        email_entry.grid(row=2, column=1, padx=10, pady=10)

        # Botão para confirmar a adição
        confirm_btn = Button(add_window, text='Adicionar', command=lambda: self.add_data(nome_entry.get(), telefone_entry.get(), email_entry.get(), add_window))
        confirm_btn.grid(row=3, column=0, columnspan=2, pady=10)
    def add_data_grupo_window(self):
        # Janela para adicionar dados
        # Cria uma nova janela chamada add_window como filha da janela principal
        # Configura a nova janela para que sua origem esteja no canto superior esquerdo da janela principal
        add_window = Toplevel(self.window)
        add_window.title('Adicionar Grupo')

        # Entradas para adicionar dados
        nome_label = Label(add_window, text='Nome do grupo:')
        nome_label.grid(row=0, column=0, padx=10, pady=10)
        nome_entry = Entry(add_window)
        nome_entry.grid(row=0, column=1, padx=10, pady=10)

        # Botão para confirmar a adição
        confirm_btn = Button(add_window, text='Adicionar', command=lambda: self.add_data_grupo(nome_entry.get(), add_window))
        confirm_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def add_data_grupo(self, nome, add_window):
        # Validar o nome do grupo
        if nome == '':
            messagebox.showerror('Erro', 'O nome do grupo não pode estar vazio.')
            return

        # Adicionar dados ao banco de dados
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO grupos (nome) VALUES (%s)', (nome,))
        self.db.commit()
        add_window.destroy()
        self.fetch_data()   
        
    
    def add_data(self, nome, telefone, email, add_window):
         if nome == '' or telefone == '' or email == '':
            messagebox.showerror('Erro', 'Todos os campos devem ser preenchidos.')
            return False

         if not re.match(r'^[0-9]+$', telefone):
            messagebox.showerror('Erro', 'O número de telefone deve conter apenas números.')
            return False

         if '@' not in email:
            messagebox.showerror('Erro', 'O e-mail deve conter um @.')
            return False

    # Adicionar dados ao banco de dados
         cursor = self.db.cursor()
         cursor.execute('INSERT INTO contatos (nome, telefone, email) VALUES (%s, %s, %s)', (nome, telefone, email))
         self.db.commit()
         add_window.destroy()
         self.fetch_data()
       
            

    
        
       
        
        
       
       

    def update_data_window(self):
        if self.table.selection():
            # Janela para atualizar dados
            update_window = Toplevel(self.window)
            update_window.title('Atualizar Contato')

   

            nome_label = Label(update_window, text='Novo Nome:')
            nome_label.grid(row=1, column=0, padx=10, pady=10)
            nome_entry = Entry(update_window)
            nome_entry.grid(row=1, column=1, padx=10, pady=10)

            telefone_label = Label(update_window, text='Novo Telefone:')
            telefone_label.grid(row=2, column=0, padx=10, pady=10)
            telefone_entry = Entry(update_window)
            telefone_entry.grid(row=2, column=1, padx=10, pady=10)

            email_label = Label(update_window, text='Novo Email:')
            email_label.grid(row=3, column=0, padx=10, pady=10)
            email_entry = Entry(update_window)
            email_entry.grid(row=3, column=1, padx=10, pady=10)

            # Botão para confirmar a atualização
            # A função self.update_data é chamada quando o botão é pressionado. Esta função atualiza os dados do usuário com base nas informações inseridas nos campos de entrada (Entry). Os argumentos da função self.update_data são os valores obtidos dos campos de entrada, bem como a janela update_window.
            #Ao executar este código, um botão chamado 'Atualizar' será exibido na janela. Quando o botão é pressionado, a função self.update_data será chamada, atualizando os dados do usuário com base nas informações inseridas
            confirm_btn = Button(update_window, text='Atualizar', command=lambda: self.update_data(nome_entry.get(), telefone_entry.get(), email_entry.get(), update_window))
            confirm_btn.grid(row=4, column=0, columnspan=2, pady=10)
        else:
    # Nenhum item selecionado, mostre uma mensagem de erro ou faça outra ação
            messagebox.showerror('Erro', 'Nenhum registro selecionado.')
     
    def update_data(self, novo_nome, novo_telefone, novo_email, update_window):
        if novo_nome == '' or novo_telefone == '' or novo_email == '':
            messagebox.showerror('Erro', 'Todos os campos devem ser preenchidos.')
            return 

        if not re.match(r'^[0-9]+$', novo_telefone):
            messagebox.showerror('Erro', 'O número de telefone deve conter apenas números.')
            return 

        if '@' not in novo_email:
            messagebox.showerror('Erro', 'O e-mail deve conter um @.')
            return 
       
        item = self.table.selection()[0]
        data = self.table.item(item, 'values')
        id = data[0]
        # Atualizar dados no banco de dados
        # o objeto 'cursor' é utilizado para executar a instrução SQL
        cursor = self.db.cursor()
        cursor.execute('UPDATE contatos SET nome=%s, telefone=%s, email=%s WHERE id=%s', (novo_nome, novo_telefone, novo_email, id))
        # Confirma a alteração no banco de dados usando a função commit
        self.db.commit()
        # Fecha a janela de atualização
        update_window.destroy()
        # Recupera os dados atualizados da tabela 'contatos' usando a função 'fetch_data'
        self.fetch_data()

    def delete_data(self):
        if self.table.selection():  # Verifica se há algum item selecionado
            item = self.table.selection()[0]
             # Pegar o ID do contato selecionado
            data = self.table.item(item, 'values')
            id = data[0]
   
      
     
        # Verificar se o usuário realmente deseja excluir o registro
            if messagebox.askyesno('Confirmação', 'Tem certeza de que deseja excluir o registro?'):
           
            # Deletar dados do banco de dados
                cursor = self.db.cursor()
                cursor.execute('DELETE FROM contatos WHERE id=%s', (id,))  # Passe o ID como uma tupla de um elemento
                self.db.commit()
                self.fetch_data()
    # ... continue seu código aqui
        else:
    # Nenhum item selecionado, mostre uma mensagem de erro ou faça outra ação
            messagebox.showerror('Erro', 'Nenhum registro selecionado.')
     
     
         # Obter o item selecionado
     
     
        
         
      
if __name__ == "__main__":
    window = Tk()
    app = CrudApp(window)
    window.mainloop()
