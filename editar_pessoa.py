import sys
import re

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QMessageBox, QGroupBox
)

from banco import conectar_pessoas


class EditarPessoa(QWidget):

    def __init__(self, id_pessoa):
        super().__init__()

        self.id_pessoa = id_pessoa

        self.setWindowTitle("Mini da Majuzita - Editar Pessoa")
        self.resize(650, 700)

        self.criar_interface()
        self.carregar_pessoa()

    def criar_interface(self):
        layout_principal = QVBoxLayout()

        titulo = QLabel("Editar Pessoa")
        titulo.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #622489;
            padding: 10px;
        """)
        layout_principal.addWidget(titulo)

        grupo = QGroupBox("Dados da pessoa")
        grid = QGridLayout()

        self.nome = QLineEdit()
        self.tipo_documento = QComboBox()
        self.tipo_documento.addItems(["CPF", "CNPJ"])
        self.documento = QLineEdit()
        self.email = QLineEdit()
        self.celular = QLineEdit()
        self.cep = QLineEdit()
        self.logradouro = QLineEdit()
        self.numero = QLineEdit()
        self.complemento = QLineEdit()
        self.bairro = QLineEdit()
        self.cidade = QLineEdit()
        self.estado = QComboBox()
        self.estado.addItems([
            "", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES",
            "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE",
            "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
        ])

        campos = [
            ("Nome completo:", self.nome),
            ("Tipo de documento:", self.tipo_documento),
            ("Documento:", self.documento),
            ("E-mail:", self.email),
            ("Celular:", self.celular),
            ("CEP:", self.cep),
            ("Logradouro:", self.logradouro),
            ("Número:", self.numero),
            ("Complemento:", self.complemento),
            ("Bairro:", self.bairro),
            ("Cidade:", self.cidade),
            ("Estado:", self.estado),
        ]

        for linha, (texto, widget) in enumerate(campos):
            grid.addWidget(QLabel(texto), linha, 0)
            grid.addWidget(widget, linha, 1)

        grupo.setLayout(grid)
        layout_principal.addWidget(grupo)

        botoes = QGridLayout()

        salvar = QPushButton("Salvar Alterações")
        cancelar = QPushButton("Cancelar")

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
        """

        salvar.setStyleSheet(estilo)
        cancelar.setStyleSheet(estilo)

        botoes.addWidget(salvar, 0, 0)
        botoes.addWidget(cancelar, 0, 1)
        layout_principal.addLayout(botoes)

        salvar.clicked.connect(self.salvar_alteracoes)
        cancelar.clicked.connect(self.close)

        self.setLayout(layout_principal)

    def carregar_pessoa(self):
        try:
            conexao = conectar_pessoas()
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT nome_completo, tipo_documento, documento, email,
                       celular, cep, logradouro, numero, complemento,
                       bairro, cidade, estado
                FROM pessoas
                WHERE id = ?
            """, (self.id_pessoa,))
            pessoa = cursor.fetchone()
            conexao.close()

            if not pessoa:
                QMessageBox.warning(
                    self, "Erro", "Pessoa não encontrada!"
                )
                self.close()
                return

            widgets = [
                self.nome, self.tipo_documento, self.documento, self.email,
                self.celular, self.cep, self.logradouro, self.numero,
                self.complemento, self.bairro, self.cidade, self.estado
            ]

            for widget, valor in zip(widgets, pessoa):
                valor = "" if valor is None else str(valor)
                if isinstance(widget, QComboBox):
                    indice = widget.findText(valor)
                    if indice >= 0:
                        widget.setCurrentIndex(indice)
                else:
                    widget.setText(valor)

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível carregar a pessoa.\n\n{erro}"
            )

    @staticmethod
    def somente_numeros(valor):
        return re.sub(r"\D", "", valor)

    def validar_documento(self, documento, tipo):
        numeros = self.somente_numeros(documento)

        if tipo == "CPF":
            if len(numeros) != 11 or len(set(numeros)) == 1:
                return False
            soma = sum(int(numeros[i]) * (10 - i) for i in range(9))
            digito1 = (soma * 10 % 11) % 10
            if digito1 != int(numeros[9]):
                return False
            soma = sum(int(numeros[i]) * (11 - i) for i in range(10))
            digito2 = (soma * 10 % 11) % 10
            return digito2 == int(numeros[10])

        if len(numeros) != 14 or len(set(numeros)) == 1:
            return False

        def calcular(base, pesos):
            soma = sum(int(n) * p for n, p in zip(base, pesos))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto

        d1 = calcular(numeros[:12], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        d2 = calcular(numeros[:12] + str(d1),
                      [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])

        return numeros[-2:] == f"{d1}{d2}"

    def salvar_alteracoes(self):
        nome = self.nome.text().strip()
        tipo = self.tipo_documento.currentText()
        documento = self.documento.text().strip()
        email = self.email.text().strip()
        celular = self.celular.text().strip()
        cep = self.cep.text().strip()
        logradouro = self.logradouro.text().strip()
        numero = self.numero.text().strip()
        complemento = self.complemento.text().strip()
        bairro = self.bairro.text().strip()
        cidade = self.cidade.text().strip()
        estado = self.estado.currentText().strip()

        if not all([
            nome, documento, email, celular, cep, logradouro,
            numero, bairro, cidade, estado
        ]):
            QMessageBox.warning(
                self, "Erro", "Preencha todos os campos obrigatórios!"
            )
            return

        if not self.validar_documento(documento, tipo):
            QMessageBox.warning(
                self, "Erro", f"{tipo} inválido!"
            )
            return

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            QMessageBox.warning(
                self, "Erro", "Digite um e-mail válido!"
            )
            return

        if len(self.somente_numeros(celular)) not in (10, 11):
            QMessageBox.warning(
                self, "Erro", "Digite um celular válido!"
            )
            return

        if len(self.somente_numeros(cep)) != 8:
            QMessageBox.warning(
                self, "Erro", "Digite um CEP válido!"
            )
            return

        try:
            conexao = conectar_pessoas()
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT id FROM pessoas
                WHERE documento = ? AND id != ?
            """, (documento, self.id_pessoa))

            if cursor.fetchone():
                conexao.close()
                QMessageBox.warning(
                    self, "Erro",
                    "Já existe outra pessoa cadastrada com este documento!"
                )
                return

            cursor.execute("""
                UPDATE pessoas
                SET nome_completo = ?,
                    tipo_documento = ?,
                    documento = ?,
                    email = ?,
                    celular = ?,
                    cep = ?,
                    logradouro = ?,
                    numero = ?,
                    complemento = ?,
                    bairro = ?,
                    cidade = ?,
                    estado = ?
                WHERE id = ?
            """, (
                nome, tipo, documento, email, celular, cep,
                logradouro, numero, complemento, bairro, cidade,
                estado, self.id_pessoa
            ))

            conexao.commit()
            conexao.close()

            QMessageBox.information(
                self, "Sucesso",
                "Pessoa atualizada com sucesso!"
            )
            self.close()

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível atualizar a pessoa.\n\n{erro}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = EditarPessoa(1)
    janela.show()
    sys.exit(app.exec())
