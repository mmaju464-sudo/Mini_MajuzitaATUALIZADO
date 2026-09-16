import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QPushButton,
    QMessageBox
)

from banco import conectar


class EditarProduto(QWidget):

    def __init__(self, id_produto):
        super().__init__()

        self.id_produto = id_produto

        self.setWindowTitle("Mini da Majuzita - Editar Produto")
        self.resize(400, 400)

        layout = QVBoxLayout()

        # ==========================
        # TÍTULO
        # ==========================

        titulo = QLabel("Editar Produto")

        titulo.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #622489;
        """)

        layout.addWidget(titulo)

        # ==========================
        # CÓDIGO
        # ==========================

        layout.addWidget(QLabel("Código de barras:"))

        self.codigo = QLineEdit()

        layout.addWidget(self.codigo)

        # ==========================
        # NOME
        # ==========================

        layout.addWidget(QLabel("Nome do Produto:"))

        self.nome = QLineEdit()

        layout.addWidget(self.nome)

        # ==========================
        # CATEGORIA
        # ==========================

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

        # ==========================
        # PREÇO
        # ==========================

        layout.addWidget(QLabel("Preço de Venda:"))

        self.preco = QLineEdit()

        layout.addWidget(self.preco)

        # ==========================
        # ESTOQUE
        # ==========================

        layout.addWidget(QLabel("Estoque:"))

        self.quantidade = QSpinBox()

        self.quantidade.setMinimum(0)
        self.quantidade.setMaximum(999999)

        layout.addWidget(self.quantidade)

        # ==========================
        # BOTÃO SALVAR
        # ==========================

        salvar = QPushButton("Salvar Alterações")

        salvar.setStyleSheet("""
            QPushButton {
                background-color: #622489;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #7a2da8;
            }
        """)

        layout.addWidget(salvar)

        salvar.clicked.connect(self.salvar_alteracoes)

        self.setLayout(layout)

        # Carrega os dados do produto
        self.carregar_produto()

    # ==========================
    # CARREGAR PRODUTO
    # ==========================

    def carregar_produto(self):

        try:

            conexao = conectar()
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT codigo, nome, categoria, preco, quantidade
                FROM produtos
                WHERE id = ?
            """, (self.id_produto,))

            produto = cursor.fetchone()

            conexao.close()

            if produto is None:

                QMessageBox.warning(
                    self,
                    "Erro",
                    "Produto não encontrado!"
                )

                self.close()
                return

            # Preenche os campos

            self.codigo.setText(str(produto[0]))

            self.nome.setText(str(produto[1]))

            categoria = self.categoria.findText(
                str(produto[2])
            )

            if categoria >= 0:
                self.categoria.setCurrentIndex(categoria)

            self.preco.setText(
                str(produto[3]).replace(".", ",")
            )

            self.quantidade.setValue(
                int(produto[4])
            )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível carregar o produto.\n\n"
                f"Erro: {erro}"
            )

    # ==========================
    # SALVAR ALTERAÇÕES
    # ==========================

    def salvar_alteracoes(self):

        codigo = self.codigo.text().strip()
        nome = self.nome.text().strip()
        categoria = self.categoria.currentText()
        preco_texto = self.preco.text().strip()
        quantidade = self.quantidade.value()

        # Verifica campos obrigatórios

        if not codigo or not nome or not preco_texto:

            QMessageBox.warning(
                self,
                "Erro",
                "Preencha todos os campos!"
            )

            return

        if categoria == "Selecione":

            QMessageBox.warning(
                self,
                "Erro",
                "Selecione uma categoria!"
            )

            return

        # Converte o preço

        try:

            preco = float(
                preco_texto.replace(",", ".")
            )

        except ValueError:

            QMessageBox.warning(
                self,
                "Erro",
                "Digite um preço válido.\n\n"
                "Exemplo: 29,90"
            )

            return

        if preco <= 0:

            QMessageBox.warning(
                self,
                "Erro",
                "O preço deve ser maior que zero!"
            )

            return

        try:

            conexao = conectar()
            cursor = conexao.cursor()

            cursor.execute("""
                UPDATE produtos
                SET
                    codigo = ?,
                    nome = ?,
                    categoria = ?,
                    preco = ?,
                    quantidade = ?
                WHERE id = ?
            """, (
                codigo,
                nome,
                categoria,
                preco,
                quantidade,
                self.id_produto
            ))

            conexao.commit()
            conexao.close()

            QMessageBox.information(
                self,
                "Sucesso",
                "Produto atualizado com sucesso!"
            )

            self.close()

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível atualizar o produto.\n\n"
                f"Erro: {erro}"
            )


# ==========================
# INICIAR A APLICAÇÃO
# ==========================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    # Para testar diretamente:
    # coloque aqui o ID de um produto existente.
    #
    # Exemplo:
    # janela = EditarProduto(1)

    janela = EditarProduto(1)

    janela.show()

    sys.exit(app.exec())
