import sqlite3


BANCO_PRODUTOS = "produtos.db"
BANCO_PESSOAS = "pessoas.db"


# ==========================================
# BANCO DE PRODUTOS
# ==========================================

def conectar():
    """
    Conecta ao banco de produtos.
    Mantemos o nome conectar()
    porque os arquivos antigos usam essa função.
    """
    return sqlite3.connect(BANCO_PRODUTOS)


def criar_tabela_produtos():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


# ==========================================
# BANCO DE PESSOAS
# ==========================================

def conectar_pessoas():
    """
    Conecta ao banco de pessoas.
    """
    return sqlite3.connect(BANCO_PESSOAS)


def criar_tabela_pessoas():

    conexao = conectar_pessoas()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo TEXT NOT NULL,
            tipo_documento TEXT NOT NULL,
            documento TEXT NOT NULL,
            email TEXT NOT NULL,
            celular TEXT NOT NULL,
            cep TEXT NOT NULL,
            logradouro TEXT NOT NULL,
            numero TEXT NOT NULL,
            complemento TEXT,
            bairro TEXT NOT NULL,
            cidade TEXT NOT NULL,
            estado TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


# ==========================================
# CRIAR OS DOIS BANCOS
# ==========================================

def criar_banco():

    criar_tabela_produtos()
    criar_tabela_pessoas()


# ==========================================
# TESTE
# ==========================================

if __name__ == "__main__":

    criar_banco()

    print("Banco de produtos criado/verificado!")
    print("Banco de pessoas criado/verificado!")
    print("Tudo certo!")