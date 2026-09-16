import sys
from PySide6.QtWidgets import *
from banco import conectar


class NovoProduto(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mini da Majuzita")
        self.resize(400, 400)

        layout = QVBoxLayout()

        # Título
        titulo = QLabel("Novo Produto")
        titulo.setStyleSheet(
            "font-size: 28px; font-weight: bold; color: #622489;"
        )
        layout.addWidget(titulo)

        # Código
        layout.addWidget(QLabel("Código de barras:"))
        self.codigo = QLineEdit()
        self.codigo.setPlaceholderText("Ex: 574527354757")
        layout.addWidget(self.codigo)

        # Nome
        layout.addWidget(QLabel("Nome do Produto:"))
        self.nome = QLineEdit()
        self.nome.setPlaceholderText("Ex: Perfume da Majuzita")
        layout.addWidget(self.nome)

        # Categoria
        layout.addWidget(QLabel("Categoria:"))
        self.categoria = QComboBox()
        self.categoria.addItems([
            "Selecione",
            "Perfumaria",
            "Outfits",
            "Beleza",
            "Joalheria"
        ])
        layout.addWidget(self.categoria)

        # Preço
        layout.addWidget(QLabel("Preço de Venda:"))
        self.preco = QLineEdit()
        self.preco.setPlaceholderText("Ex: 29.90")
        layout.addWidget(self.preco)

        # Estoque
        layout.addWidget(QLabel("Estoque Inicial:"))
        self.quantidade = QSpinBox()
        self.quantidade.setMinimum(1)
        layout.addWidget(self.quantidade)

        # Botão Limpar
        limpar = QPushButton("Limpar")
        limpar.setStyleSheet(
            "background-color: #622489; "
            "color: white; "
            "font-weight: bold;"
        )
        layout.addWidget(limpar)

        # Botão Salvar
        salvar = QPushButton("Salvar Produto")
        salvar.setStyleSheet(
            "background-color: #622489; "
            "color: white; "
            "font-weight: bold;"
        )
        layout.addWidget(salvar)

        # Conecta os botões às funções
        limpar.clicked.connect(self.limpar)
        salvar.clicked.connect(self.salvar)

        self.setLayout(layout)

    def limpar(self):
        """Limpa todos os campos do formulário."""
        self.codigo.clear()
        self.nome.clear()
        self.preco.clear()
        self.categoria.setCurrentIndex(0)
        self.quantidade.setValue(1)

    def salvar(self):
        """Salva o produto no banco de dados."""

        # Verifica os campos obrigatórios
        if (
            not self.codigo.text().strip()
            or not self.nome.text().strip()
            or not self.preco.text().strip()
            or self.categoria.currentText() == "Selecione"
        ):
            QMessageBox.warning(
                self,
                "Erro",
                "Preencha todos os campos!"
            )
            return

        # Converte o preço para número
        try:
            preco = float(
                self.preco.text().replace(",", ".")
            )
        except ValueError:
            QMessageBox.warning(
                self,
                "Erro",
                "Digite um preço válido.\n"
                "Exemplo: 29.90"
            )
            return

        # Verifica se o preço é positivo
        if preco <= 0:
            QMessageBox.warning(
                self,
                "Erro",
                "O preço deve ser maior que zero!"
            )
            return

        # Pega os dados do formulário
        codigo = self.codigo.text().strip()
        nome = self.nome.text().strip()
        categoria = self.categoria.currentText()
        quantidade = self.quantidade.value()

        try:
            # Conecta ao banco
            conexao = conectar()
            cursor = conexao.cursor()

            # Insere o produto
            cursor.execute("""
                INSERT INTO produtos
                (codigo, nome, categoria, preco, quantidade)
                VALUES (?, ?, ?, ?, ?)
            """, (
                codigo,
                nome,
                categoria,
                preco,
                quantidade
            ))

            # Confirma a gravação
            conexao.commit()

            # Fecha o banco
            conexao.close()

            # Mensagem de sucesso
            QMessageBox.information(
                self,
                "Sucesso",
                "Produto salvo com sucesso no banco de dados!"
            )

            # Limpa o formulário
            self.limpar()

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível salvar o produto.\n\n"
                f"Erro: {erro}"
            )


# Inicia o aplicativo somente quando este arquivo for executado diretamente
if __name__ == "__main__":
    app = QApplication(sys.argv)

    janela = NovoProduto()
    janela.show()

    sys.exit(app.exec())

