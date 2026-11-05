from app.models.user_account import UserAccount
from app.models.produto import Produto
import sqlite3
import uuid


class DataRecord():
    """Banco de dados SQLite para os recursos Usuários e Produtos"""

    DB_PATH = "app/controllers/db/banco.db"

    def __init__(self):

        self.__authenticated_users = {}
        self.__conn = sqlite3.connect(self.DB_PATH, check_same_thread=False)
        self.__conn.row_factory = sqlite3.Row
        self.__create_tables()


    def __create_tables(self):
        self.__conn.execute("""
            CREATE TABLE IF NOT EXISTS user_account (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )""")
        self.__conn.execute("""
            CREATE TABLE IF NOT EXISTS produto (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                nome  TEXT NOT NULL,
                preco REAL NOT NULL
            )""")
        # usuário padrão do portal: admin / admin
        self.__conn.execute("INSERT OR IGNORE INTO user_account VALUES ('admin', 'admin')")
        self.__conn.commit()


    # ---------------- Usuários ----------------

    def getCurrentUser(self, session_id):
        return self.__authenticated_users.get(session_id)


    def checkUser(self, username, password):
        linha = self.__conn.execute(
            "SELECT * FROM user_account WHERE username = ? AND password = ?",
            (username, password)).fetchone()
        if linha:
            user = UserAccount(linha['username'], linha['password'])
            session_id = str(uuid.uuid4())  # Gera um ID de sessão único
            self.__authenticated_users[session_id] = user
            return session_id
        return None


    def logout(self, session_id):
        self.__authenticated_users.pop(session_id, None)


    # ---------------- Produtos ----------------

    def getProdutos(self):
        linhas = self.__conn.execute("SELECT * FROM produto ORDER BY id").fetchall()
        return [Produto(l['id'], l['nome'], l['preco']) for l in linhas]


    def addProduto(self, nome, preco):
        cursor = self.__conn.execute("INSERT INTO produto (nome, preco) VALUES (?, ?)", (nome, preco))
        self.__conn.commit()
        return Produto(cursor.lastrowid, nome, preco)


    def deleteProduto(self, id):
        cursor = self.__conn.execute("DELETE FROM produto WHERE id = ?", (id,))
        self.__conn.commit()
        return cursor.rowcount > 0
