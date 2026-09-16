import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView
)

from banco import conectar
from editar_produto import EditarProduto


class ListaProdutos(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mini da Majuzita - Produtos")
        self.resize(900, 550)

        # Guarda a janela de edição
        self.janela_edicao = None

        # ==========================
        # LAYOUT PRINCIPAL
        # ==========================

        layout = QVBoxLayout()

        # ==========================
        # TÍTULO
        # ==========================

        titulo = QLabel("Produtos Cadastrados")

        titulo.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #622489;
            margin-bottom: 10px;
        """)

        layout.addWidget(titulo)

        # ==========================
        # TABELA
        # ==========================

        self.tabela = QTableWidget()

        self.tabela.setColumnCount(6)

        self.tabela.setHorizontalHeaderLabels([
            "ID",
            "Código",
            "Produto",
            "Categoria",
            "Preço",
            "Estoque"
        ])

        # Ajusta as colunas automaticamente
        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        # Não permite editar diretamente na tabela
        self.tabela.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        # Seleciona a linha inteira
        self.tabela.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        # Permite selecionar somente uma linha
        self.tabela.setSelectionMode(
            QTableWidget.SingleSelection
        )

        layout.addWidget(self.tabela)

        # ==========================
        # BOTÕES
        # ==========================

        botoes = QHBoxLayout()

        self.botao_atualizar = QPushButton(" Atualizar Lista")
        self.botao_editar = QPushButton(" Editar Produto")
        self.botao_excluir = QPushButton(" Excluir Produto")

        estilo_botao = """
            QPushButton {
                background-color: #622489;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 6px;
            }

            QPushButton:hover {
                background-color: #7a2da8;
            }

            QPushButton:pressed {
                background-color: #4d1b6d;
            }
        """

        self.botao_atualizar.setStyleSheet(estilo_botao)
        self.botao_editar.setStyleSheet(estilo_botao)
        self.botao_excluir.setStyleSheet(estilo_botao)

        botoes.addWidget(self.botao_atualizar)
        botoes.addWidget(self.botao_editar)
        botoes.addWidget(self.botao_excluir)

        layout.addLayout(botoes)

        # ==========================
        # CONECTAR BOTÕES
        # ==========================

        self.botao_atualizar.clicked.connect(
            self.carregar_produtos
        )

        self.botao_editar.clicked.connect(
            self.editar_produto
        )

        self.botao_excluir.clicked.connect(
            self.excluir_produto
        )

        self.setLayout(layout)

        # ==========================
        # CARREGAR PRODUTOS
        # ==========================

        self.carregar_produtos()

    # ==========================
    # CARREGAR PRODUTOS
    # ==========================

    def carregar_produtos(self):

        try:

            conexao = conectar()
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT
                    id,
                    codigo,
                    nome,
                    categoria,
                    preco,
                    quantidade
                FROM produtos
                ORDER BY id DESC
            """)

            produtos = cursor.fetchall()

            conexao.close()

            # Limpa a tabela
            self.tabela.clearContents()
            self.tabela.setRowCount(0)

            # Adiciona os produtos
            for produto in produtos:

                linha = self.tabela.rowCount()

                self.tabela.insertRow(linha)

                # ID
                self.tabela.setItem(
                    linha,
                    0,
                    QTableWidgetItem(str(produto[0]))
                )

                # Código
                self.tabela.setItem(
                    linha,
                    1,
                    QTableWidgetItem(str(produto[1]))
                )

                # Nome
                self.tabela.setItem(
                    linha,
                    2,
                    QTableWidgetItem(str(produto[2]))
                )

                # Categoria
                self.tabela.setItem(
                    linha,
                    3,
                    QTableWidgetItem(str(produto[3]))
                )

                # Preço
                self.tabela.setItem(
                    linha,
                    4,
                    QTableWidgetItem(
                        f"R$ {produto[4]:.2f}".replace(".", ",")
                    )
                )

                # Estoque
                self.tabela.setItem(
                    linha,
                    5,
                    QTableWidgetItem(str(produto[5]))
                )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível carregar os produtos.\n\n"
                f"Erro: {erro}"
            )

    # ==========================
    # EDITAR PRODUTO
    # ==========================

    def editar_produto(self):

        # Descobre qual linha foi selecionada
        linha = self.tabela.currentRow()

        if linha < 0:

            QMessageBox.warning(
                self,
                "Atenção",
                "Selecione um produto para editar."
            )

            return

        # Pega o ID do produto
        item_id = self.tabela.item(linha, 0)

        if item_id is None:

            QMessageBox.warning(
                self,
                "Erro",
                "Não foi possível identificar o produto."
            )

            return

        id_produto = int(item_id.text())

        # Abre a tela de edição
        self.janela_edicao = EditarProduto(id_produto)

        # Quando fechar a edição, atualiza a lista
        self.janela_edicao.destroyed.connect(
            self.carregar_produtos
        )

        self.janela_edicao.show()

    # ==========================
    # EXCLUIR PRODUTO
    # ==========================

    def excluir_produto(self):

        # Descobre qual linha foi selecionada
        linha = self.tabela.currentRow()

        if linha < 0:

            QMessageBox.warning(
                self,
                "Atenção",
                "Selecione um produto para excluir."
            )

            return

        # Pega o ID
        item_id = self.tabela.item(linha, 0)

        if item_id is None:

            QMessageBox.warning(
                self,
                "Erro",
                "Não foi possível identificar o produto."
            )

            return

        id_produto = int(item_id.text())

        # Pega o nome
        item_nome = self.tabela.item(linha, 2)

        if item_nome:
            nome_produto = item_nome.text()
        else:
            nome_produto = "este produto"

        # Confirmação
        resposta = QMessageBox.question(
            self,
            "Confirmar exclusão",
            f"Tem certeza que deseja excluir:\n\n"
            f"{nome_produto}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if resposta == QMessageBox.No:
            return

        try:

            conexao = conectar()
            cursor = conexao.cursor()

            cursor.execute(
                "DELETE FROM produtos WHERE id = ?",
                (id_produto,)
            )

            conexao.commit()
            conexao.close()

            QMessageBox.information(
                self,
                "Sucesso",
                "Produto excluído com sucesso!"
            )

            # Atualiza a tabela
            self.carregar_produtos()

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível excluir o produto.\n\n"
                f"Erro: {erro}"
            )


# ==========================
# INICIAR A APLICAÇÃO
# ==========================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    janela = ListaProdutos()

    janela.show()

    sys.exit(app.exec())