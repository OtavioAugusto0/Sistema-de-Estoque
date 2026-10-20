import sqlite3
import customtkinter as ctk
from tkinter import messagebox


# =========================
# CONFIGURAÇÃO
# =========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =========================
# BANCO DE DADOS
# =========================

conexao = sqlite3.connect("BancoDeDados.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Estoque (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    preco REAL NOT NULL
)
""")

conexao.commit()


# =========================
# CLASSE PRINCIPAL
# =========================

class Estoque:

    def __init__(self, app):

        self.app = app

        # Título
        self.titulo = ctk.CTkLabel(
            app,
            text="Sistema de Gerenciamento de Estoque",
            font=("Arial", 26, "bold")
        )

        self.titulo.pack(pady=30)


        # Botão adicionar
        self.button_add = ctk.CTkButton(
            app,
            text="Adicionar Produto",
            font=("Arial", 16),
            width=250,
            height=40,
            command=self.add_produto
        )

        self.button_add.pack(pady=10)


        # Botão visualizar
        self.button_view = ctk.CTkButton(
            app,
            text="Visualizar Estoque",
            font=("Arial", 16),
            width=250,
            height=40,
            command=self.visualizar_estoque
        )

        self.button_view.pack(pady=10)


        # Botão atualizar
        self.button_update = ctk.CTkButton(
            app,
            text="Atualizar Produto",
            font=("Arial", 16),
            width=250,
            height=40,
            command=self.atualizar_produto
        )

        self.button_update.pack(pady=10)


        # Botão remover
        self.button_remove = ctk.CTkButton(
            app,
            text="Remover Produto",
            font=("Arial", 16),
            width=250,
            height=40,
            command=self.remover_produto
        )

        self.button_remove.pack(pady=10)


        # Botão sair
        self.button_exit = ctk.CTkButton(
            app,
            text="Sair",
            font=("Arial", 16),
            width=250,
            height=40,
            command=self.sair
        )

        self.button_exit.pack(pady=10)


    # =========================
    # CONFIGURAR JANELA
    # =========================

    def configurar_janela(self, janela):

        janela.transient(self.app)
        janela.lift()
        janela.focus_force()
        janela.grab_set()


    # =========================
    # ADICIONAR PRODUTO
    # =========================

    def add_produto(self):

        janela = ctk.CTkToplevel(self.app)

        janela.title("Adicionar Produto")
        janela.geometry("400x400")

        self.configurar_janela(janela)


        titulo = ctk.CTkLabel(
            janela,
            text="Adicionar Produto",
            font=("Arial", 22, "bold")
        )

        titulo.pack(pady=20)


        entrada_nome = ctk.CTkEntry(
            janela,
            placeholder_text="Nome do produto",
            width=300
        )

        entrada_nome.pack(pady=10)


        entrada_quantidade = ctk.CTkEntry(
            janela,
            placeholder_text="Quantidade",
            width=300
        )

        entrada_quantidade.pack(pady=10)


        entrada_preco = ctk.CTkEntry(
            janela,
            placeholder_text="Preço",
            width=300
        )

        entrada_preco.pack(pady=10)


        def cadastrar():

            nome = entrada_nome.get()
            quantidade = entrada_quantidade.get()
            preco = entrada_preco.get()


            if nome == "" or quantidade == "" or preco == "":

                messagebox.showwarning(
                    "Atenção",
                    "Preencha todos os campos.",
                    parent=janela
                )

                return


            try:

                quantidade = int(quantidade)
                preco = float(preco)

            except ValueError:

                messagebox.showerror(
                    "Erro",
                    "Quantidade deve ser um número inteiro e preço deve ser um número.",
                    parent=janela
                )

                return


            cursor.execute(
                """
                INSERT INTO Estoque
                (nome, quantidade, preco)
                VALUES (?, ?, ?)
                """,
                (nome, quantidade, preco)
            )

            conexao.commit()


            messagebox.showinfo(
                "Sucesso",
                "Produto cadastrado com sucesso!",
                parent=janela
            )

            janela.destroy()


        botao_cadastrar = ctk.CTkButton(
            janela,
            text="Cadastrar",
            width=200,
            height=40,
            command=cadastrar
        )

        botao_cadastrar.pack(pady=20)


    # =========================
    # VISUALIZAR ESTOQUE
    # =========================

    def visualizar_estoque(self):

        janela = ctk.CTkToplevel(self.app)

        janela.title("Estoque")
        janela.geometry("700x500")

        self.configurar_janela(janela)


        titulo = ctk.CTkLabel(
            janela,
            text="Estoque de Produtos",
            font=("Arial", 24, "bold")
        )

        titulo.pack(pady=20)


        cursor.execute("SELECT * FROM Estoque")

        produtos = cursor.fetchall()


        if not produtos:

            label = ctk.CTkLabel(
                janela,
                text="Nenhum produto cadastrado.",
                font=("Arial", 16)
            )

            label.pack(pady=30)

            return


        for produto in produtos:

            id_produto = produto[0]
            nome = produto[1]
            quantidade = produto[2]
            preco = produto[3]


            texto = (
                f"ID: {id_produto}   |   "
                f"Produto: {nome}   |   "
                f"Quantidade: {quantidade}   |   "
                f"Preço: R$ {preco:.2f}"
            )


            label = ctk.CTkLabel(
                janela,
                text=texto,
                font=("Arial", 14)
            )

            label.pack(pady=5)


    # =========================
    # ATUALIZAR PRODUTO
    # =========================

    def atualizar_produto(self):

        janela = ctk.CTkToplevel(self.app)

        janela.title("Atualizar Produto")
        janela.geometry("400x450")

        self.configurar_janela(janela)


        titulo = ctk.CTkLabel(
            janela,
            text="Atualizar Produto",
            font=("Arial", 22, "bold")
        )

        titulo.pack(pady=20)


        entrada_id = ctk.CTkEntry(
            janela,
            placeholder_text="ID do produto",
            width=300
        )

        entrada_id.pack(pady=10)


        entrada_nome = ctk.CTkEntry(
            janela,
            placeholder_text="Novo nome",
            width=300
        )

        entrada_nome.pack(pady=10)


        entrada_quantidade = ctk.CTkEntry(
            janela,
            placeholder_text="Nova quantidade",
            width=300
        )

        entrada_quantidade.pack(pady=10)


        entrada_preco = ctk.CTkEntry(
            janela,
            placeholder_text="Novo preço",
            width=300
        )

        entrada_preco.pack(pady=10)


        def atualizar():

            id_produto = entrada_id.get()
            nome = entrada_nome.get()
            quantidade = entrada_quantidade.get()
            preco = entrada_preco.get()


            if (
                id_produto == ""
                or nome == ""
                or quantidade == ""
                or preco == ""
            ):

                messagebox.showwarning(
                    "Atenção",
                    "Preencha todos os campos.",
                    parent=janela
                )

                return


            try:

                id_produto = int(id_produto)
                quantidade = int(quantidade)
                preco = float(preco)

            except ValueError:

                messagebox.showerror(
                    "Erro",
                    "Verifique os valores digitados.",
                    parent=janela
                )

                return


            cursor.execute(
                """
                UPDATE Estoque
                SET nome = ?, quantidade = ?, preco = ?
                WHERE id = ?
                """,
                (
                    nome,
                    quantidade,
                    preco,
                    id_produto
                )
            )

            conexao.commit()


            if cursor.rowcount == 0:

                messagebox.showwarning(
                    "Atenção",
                    "Produto não encontrado.",
                    parent=janela
                )

                return


            messagebox.showinfo(
                "Sucesso",
                "Produto atualizado com sucesso!",
                parent=janela
            )

            janela.destroy()


        botao = ctk.CTkButton(
            janela,
            text="Atualizar",
            width=200,
            height=40,
            command=atualizar
        )

        botao.pack(pady=20)


    # =========================
    # REMOVER PRODUTO
    # =========================

    def remover_produto(self):

        janela = ctk.CTkToplevel(self.app)

        janela.title("Remover Produto")
        janela.geometry("400x300")

        self.configurar_janela(janela)


        titulo = ctk.CTkLabel(
            janela,
            text="Remover Produto",
            font=("Arial", 22, "bold")
        )

        titulo.pack(pady=30)


        entrada_id = ctk.CTkEntry(
            janela,
            placeholder_text="ID do produto",
            width=300
        )

        entrada_id.pack(pady=10)


        def remover():

            id_produto = entrada_id.get()


            if id_produto == "":

                messagebox.showwarning(
                    "Atenção",
                    "Digite o ID do produto.",
                    parent=janela
                )

                return


            try:

                id_produto = int(id_produto)

            except ValueError:

                messagebox.showerror(
                    "Erro",
                    "O ID deve ser um número.",
                    parent=janela
                )

                return


            confirmar = messagebox.askyesno(
                "Confirmar",
                "Tem certeza que deseja remover este produto?",
                parent=janela
            )


            if not confirmar:

                return


            cursor.execute(
                "DELETE FROM Estoque WHERE id = ?",
                (id_produto,)
            )

            conexao.commit()


            if cursor.rowcount == 0:

                messagebox.showwarning(
                    "Atenção",
                    "Produto não encontrado.",
                    parent=janela
                )

                return


            messagebox.showinfo(
                "Sucesso",
                "Produto removido com sucesso!",
                parent=janela
            )

            janela.destroy()


        botao = ctk.CTkButton(
            janela,
            text="Remover",
            width=200,
            height=40,
            command=remover
        )

        botao.pack(pady=20)


    # =========================
    # SAIR
    # =========================

    def sair(self):

        conexao.close()

        self.app.destroy()


# =========================
# JANELA PRINCIPAL
# =========================

app = ctk.CTk()

app.title("Sistema de Gerenciamento de Estoque")

app.geometry("800x600")


# Cria o sistema
estoque = Estoque(app)


# Executa a aplicação
app.mainloop()