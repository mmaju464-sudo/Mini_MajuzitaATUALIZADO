import sys

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
)

from banco import criar_banco
from produtos import NovoProduto
from lista_produtos import ListaProdutos
from cadastro import CadastroPessoa
from lista_pessoas import ListaPessoas


class MenuPrincipal(QWidget):

    def __init__(self):
        super().__init__()

        criar_banco()

        self.setWindowTitle("Mini da Majuzita")
        self.resize(500, 500)

        self.janelas = []

        layout = QVBoxLayout()

        titulo = QLabel("Mini da Majuzita")
        titulo.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
            color: #622489;
            padding: 15px;
        """)
        layout.addWidget(titulo)

        subtitulo = QLabel("Sistema de cadastro")
        subtitulo.setStyleSheet("font-size: 16px;")
        layout.addWidget(subtitulo)

        botoes = [
            ("Cadastrar Produto", NovoProduto),
            ("Lista de Produtos", ListaProdutos),
            ("Cadastrar Pessoa", CadastroPessoa),
            ("Lista de Pessoas - CRUD", ListaPessoas),
        ]

        estilo = """
            QPushButton {
                background-color: #622489;
                color: white;
                font-weight: bold;
                font-size: 15px;
                padding: 13px;
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: #7a2da8;
            }
            QPushButton:pressed {
                background-color: #4d1b6d;
            }
        """

        for texto, classe in botoes:
            botao = QPushButton(texto)
            botao.setStyleSheet(estilo)
            botao.clicked.connect(
                lambda checked=False, c=classe: self.abrir(c)
            )
            layout.addWidget(botao)

        self.setLayout(layout)

    def abrir(self, classe):
        janela = classe()
        self.janelas.append(janela)
        janela.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = MenuPrincipal()
    janela.show()
    sys.exit(app.exec())
