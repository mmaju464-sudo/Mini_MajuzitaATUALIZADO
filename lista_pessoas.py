import sys

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView
)

from banco import conectar_pessoas
from editar_pessoa import EditarPessoa


class ListaPessoas(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mini da Majuzita - Pessoas")
        self.resize(1200, 650)
        self.janela_edicao = None

        layout = QVBoxLayout()

        titulo = QLabel("Pessoas Cadastradas")
        titulo.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #622489;
            padding: 10px;
        """)
        layout.addWidget(titulo)

        # Campo de filtro
        self.filtro = QLineEdit()
        self.filtro.setPlaceholderText(
            "Digite uma palavra para filtrar as pessoas..."
        )
        layout.addWidget(self.filtro)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(13)
        self.tabela.setHorizontalHeaderLabels([
            "ID", "Nome", "Tipo", "Documento", "E-mail", "Celular",
            "CEP", "Logradouro", "Número", "Complemento",
            "Bairro", "Cidade", "Estado"
        ])
        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.tabela.horizontalHeader().setStretchLastSection(True)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.tabela)

        botoes = QHBoxLayout()

        self.botao_atualizar = QPushButton("Atualizar Lista")
        self.botao_editar = QPushButton("Editar Pessoa")
        self.botao_excluir = QPushButton("Excluir Pessoa")
        self.botao_pdf = QPushButton("Exportar para PDF")

        estilo = """
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

        for botao in (
            self.botao_atualizar,
            self.botao_editar,
            self.botao_excluir,
            self.botao_pdf
        ):
            botao.setStyleSheet(estilo)
            botoes.addWidget(botao)

        layout.addLayout(botoes)
        self.setLayout(layout)

        self.filtro.textChanged.connect(self.carregar_pessoas)
        self.botao_atualizar.clicked.connect(self.carregar_pessoas)
        self.botao_editar.clicked.connect(self.editar_pessoa)
        self.botao_excluir.clicked.connect(self.excluir_pessoa)
        self.botao_pdf.clicked.connect(self.exportar_pdf)

        self.carregar_pessoas()

    def carregar_pessoas(self):
        try:
            conexao = conectar_pessoas()
            cursor = conexao.cursor()

            texto = self.filtro.text().strip()
            if texto:
                pesquisa = f"%{texto}%"
                cursor.execute("""
                    SELECT id, nome_completo, tipo_documento, documento,
                           email, celular, cep, logradouro, numero,
                           complemento, bairro, cidade, estado
                    FROM pessoas
                    WHERE nome_completo LIKE ?
                       OR tipo_documento LIKE ?
                       OR documento LIKE ?
                       OR email LIKE ?
                       OR celular LIKE ?
                       OR cep LIKE ?
                       OR logradouro LIKE ?
                       OR numero LIKE ?
                       OR complemento LIKE ?
                       OR bairro LIKE ?
                       OR cidade LIKE ?
                       OR estado LIKE ?
                    ORDER BY id DESC
                """, (pesquisa,) * 12)
            else:
                cursor.execute("""
                    SELECT id, nome_completo, tipo_documento, documento,
                           email, celular, cep, logradouro, numero,
                           complemento, bairro, cidade, estado
                    FROM pessoas
                    ORDER BY id DESC
                """)

            pessoas = cursor.fetchall()
            conexao.close()

            self.tabela.setRowCount(0)

            for pessoa in pessoas:
                linha = self.tabela.rowCount()
                self.tabela.insertRow(linha)

                for coluna, valor in enumerate(pessoa):
                    self.tabela.setItem(
                        linha,
                        coluna,
                        QTableWidgetItem("" if valor is None else str(valor))
                    )

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível carregar as pessoas.\n\n{erro}"
            )

    def id_selecionado(self):
        linha = self.tabela.currentRow()

        if linha < 0:
            QMessageBox.warning(
                self,
                "Atenção",
                "Selecione uma pessoa na tabela."
            )
            return None

        return int(self.tabela.item(linha, 0).text())

    def editar_pessoa(self):
        id_pessoa = self.id_selecionado()
        if id_pessoa is None:
            return

        self.janela_edicao = EditarPessoa(id_pessoa)
        self.janela_edicao.destroyed.connect(self.carregar_pessoas)
        self.janela_edicao.show()

    def excluir_pessoa(self):
        id_pessoa = self.id_selecionado()
        if id_pessoa is None:
            return

        resposta = QMessageBox.question(
            self,
            "Confirmar exclusão",
            "Tem certeza que deseja excluir esta pessoa?",
            QMessageBox.Yes | QMessageBox.No
        )

        if resposta != QMessageBox.Yes:
            return

        try:
            conexao = conectar_pessoas()
            cursor = conexao.cursor()
            cursor.execute(
                "DELETE FROM pessoas WHERE id = ?",
                (id_pessoa,)
            )
            conexao.commit()
            conexao.close()

            QMessageBox.information(
                self,
                "Sucesso",
                "Pessoa excluída com sucesso!"
            )
            self.carregar_pessoas()

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível excluir a pessoa.\n\n{erro}"
            )

    def exportar_pdf(self):
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
            from reportlab.lib.enums import TA_CENTER
            from PySide6.QtWidgets import QFileDialog

            caminho, _ = QFileDialog.getSaveFileName(
                self,
                "Salvar PDF",
                "pessoas.pdf",
                "Arquivos PDF (*.pdf)"
            )

            if not caminho:
                return

            dados = []
            cabecalho = [
                "ID", "Nome", "Tipo", "Documento", "E-mail", "Celular",
                "CEP", "Logradouro", "Número", "Complemento",
                "Bairro", "Cidade", "Estado"
            ]
            dados.append(cabecalho)

            for linha in range(self.tabela.rowCount()):
                dados.append([
                    self.tabela.item(linha, coluna).text()
                    if self.tabela.item(linha, coluna) else ""
                    for coluna in range(self.tabela.columnCount())
                ])

            doc = SimpleDocTemplate(
                caminho,
                pagesize=landscape(A4),
                rightMargin=18,
                leftMargin=18,
                topMargin=18,
                bottomMargin=18
            )

            estilos = getSampleStyleSheet()
            titulo_style = estilos["Title"]
            titulo_style.alignment = TA_CENTER
            titulo_style.fontSize = 16

            titulo = Paragraph("Pessoas Cadastradas - Mini da Majuzita", titulo_style)

            tabela = Table(dados, repeatRows=1)
            tabela.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#622489")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 6),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1),
                 [colors.white, colors.HexColor("#f1eafa")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ]))

            doc.build([titulo, tabela])

            QMessageBox.information(
                self,
                "PDF criado",
                f"Dados exportados com sucesso!\n\nArquivo:\n{caminho}"
            )

        except ImportError:
            QMessageBox.critical(
                self,
                "Erro",
                "A biblioteca ReportLab não está instalada.\n\n"
                "Execute:\npip install reportlab"
            )
        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível exportar o PDF.\n\n{erro}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = ListaPessoas()
    janela.show()
    sys.exit(app.exec())
