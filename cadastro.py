import sys
import re
import json

from urllib.request import urlopen
from urllib.error import URLError, HTTPError

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox
)

from banco import conectar_pessoas, criar_banco

class CadastroPessoa(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mini da Majuzita - Cadastro de Pessoa")
        self.resize(650, 700)

        self.criar_interface()

    # ==========================================
    # INTERFACE
    # ==========================================

    def criar_interface(self):

        layout_principal = QVBoxLayout()

        # ==========================================
        # TÍTULO
        # ==========================================

        titulo = QLabel("Cadastro de Pessoa")

        titulo.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #622489;
                padding: 10px;
            }
        """)

        layout_principal.addWidget(titulo)

        # ==========================================
        # DADOS PESSOAIS
        # ==========================================

        grupo_pessoal = QGroupBox("Dados pessoais")

        grid_pessoal = QGridLayout()

        # Nome
        grid_pessoal.addWidget(
            QLabel("Nome completo:*"),
            0,
            0
        )

        self.nome = QLineEdit()
        self.nome.setPlaceholderText(
            "Digite o nome completo"
        )

        grid_pessoal.addWidget(
            self.nome,
            0,
            1,
            1,
            2
        )

        # Documento
        grid_pessoal.addWidget(
            QLabel("Documento:*"),
            1,
            0
        )

        self.tipo_documento = QComboBox()

        self.tipo_documento.addItems([
            "CPF",
            "CNPJ"
        ])

        grid_pessoal.addWidget(
            self.tipo_documento,
            1,
            1
        )

        self.documento = QLineEdit()

        self.documento.setPlaceholderText(
            "Digite o CPF"
        )

        grid_pessoal.addWidget(
            self.documento,
            1,
            2
        )

        # E-mail
        grid_pessoal.addWidget(
            QLabel("E-mail:*"),
            2,
            0
        )

        self.email = QLineEdit()

        self.email.setPlaceholderText(
            "exemplo@email.com"
        )

        grid_pessoal.addWidget(
            self.email,
            2,
            1,
            1,
            2
        )

        # Celular
        grid_pessoal.addWidget(
            QLabel("Celular:*"),
            3,
            0
        )

        self.celular = QLineEdit()

        self.celular.setPlaceholderText(
            "(11) 99999-9999"
        )

        grid_pessoal.addWidget(
            self.celular,
            3,
            1,
            1,
            2
        )

        grupo_pessoal.setLayout(grid_pessoal)

        layout_principal.addWidget(
            grupo_pessoal
        )

        # ==========================================
        # ENDEREÇO
        # ==========================================

        grupo_endereco = QGroupBox("Endereço")

        grid_endereco = QGridLayout()

        # CEP
        grid_endereco.addWidget(
            QLabel("CEP:*"),
            0,
            0
        )

        self.cep = QLineEdit()

        self.cep.setPlaceholderText(
            "00000-000"
        )

        grid_endereco.addWidget(
            self.cep,
            0,
            1
        )

        self.botao_cep = QPushButton(
            "Consultar CEP"
        )

        self.botao_cep.setStyleSheet("""
            QPushButton {
                background-color: #622489;
                color: white;
                font-weight: bold;
                padding: 8px;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #7a2da8;
            }

            QPushButton:pressed {
                background-color: #4d1b6d;
            }
        """)

        grid_endereco.addWidget(
            self.botao_cep,
            0,
            2
        )

        # Logradouro
        grid_endereco.addWidget(
            QLabel("Logradouro:*"),
            1,
            0
        )

        self.logradouro = QLineEdit()

        self.logradouro.setPlaceholderText(
            "Rua, avenida, etc."
        )

        grid_endereco.addWidget(
            self.logradouro,
            1,
            1,
            1,
            2
        )

        # Número
        grid_endereco.addWidget(
            QLabel("Número:*"),
            2,
            0
        )

        self.numero = QLineEdit()

        self.numero.setPlaceholderText(
            "Número"
        )

        grid_endereco.addWidget(
            self.numero,
            2,
            1
        )

        # Complemento
        grid_endereco.addWidget(
            QLabel("Complemento:"),
            3,
            0
        )

        self.complemento = QLineEdit()

        self.complemento.setPlaceholderText(
            "Apartamento, bloco, etc."
        )

        grid_endereco.addWidget(
            self.complemento,
            3,
            1,
            1,
            2
        )

        # Bairro
        grid_endereco.addWidget(
            QLabel("Bairro:*"),
            4,
            0
        )

        self.bairro = QLineEdit()

        grid_endereco.addWidget(
            self.bairro,
            4,
            1,
            1,
            2
        )

        # Cidade
        grid_endereco.addWidget(
            QLabel("Cidade:*"),
            5,
            0
        )

        self.cidade = QLineEdit()

        grid_endereco.addWidget(
            self.cidade,
            5,
            1,
            1,
            2
        )

        # Estado
        grid_endereco.addWidget(
            QLabel("Estado:*"),
            6,
            0
        )

        self.estado = QComboBox()

        self.estado.addItem(
            "Selecione"
        )

        estados = [
            "AC - Acre",
            "AL - Alagoas",
            "AP - Amapá",
            "AM - Amazonas",
            "BA - Bahia",
            "CE - Ceará",
            "DF - Distrito Federal",
            "ES - Espírito Santo",
            "GO - Goiás",
            "MA - Maranhão",
            "MT - Mato Grosso",
            "MS - Mato Grosso do Sul",
            "MG - Minas Gerais",
            "PA - Pará",
            "PB - Paraíba",
            "PR - Paraná",
            "PE - Pernambuco",
            "PI - Piauí",
            "RJ - Rio de Janeiro",
            "RN - Rio Grande do Norte",
            "RS - Rio Grande do Sul",
            "RO - Rondônia",
            "RR - Roraima",
            "SC - Santa Catarina",
            "SP - São Paulo",
            "SE - Sergipe",
            "TO - Tocantins"
        ]

        self.estado.addItems(estados)

        grid_endereco.addWidget(
            self.estado,
            6,
            1,
            1,
            2
        )

        grupo_endereco.setLayout(
            grid_endereco
        )

        layout_principal.addWidget(
            grupo_endereco
        )

        # ==========================================
        # BOTÕES
        # ==========================================

        botoes = QHBoxLayout()

        self.botao_limpar = QPushButton(
            "Limpar"
        )

        self.botao_salvar = QPushButton(
            "Salvar Cadastro"
        )

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

        self.botao_limpar.setStyleSheet(
            estilo
        )

        self.botao_salvar.setStyleSheet(
            estilo
        )

        botoes.addWidget(
            self.botao_limpar
        )

        botoes.addWidget(
            self.botao_salvar
        )

        layout_principal.addLayout(
            botoes
        )

        # ==========================================
        # AVISO
        # ==========================================

        aviso = QLabel(
            "* Campos obrigatórios"
        )

        aviso.setStyleSheet("""
            color: #666666;
            font-size: 12px;
        """)

        layout_principal.addWidget(
            aviso
        )

        self.setLayout(
            layout_principal
        )

        # ==========================================
        # EVENTOS
        # ==========================================

        self.botao_cep.clicked.connect(
            self.consultar_cep
        )

        self.botao_limpar.clicked.connect(
            self.limpar
        )

        self.botao_salvar.clicked.connect(
            self.salvar
        )

        self.tipo_documento.currentTextChanged.connect(
            self.alterar_placeholder_documento
        )

    # ==========================================
    # PLACEHOLDER DOCUMENTO
    # ==========================================

    def alterar_placeholder_documento(self):

        if self.tipo_documento.currentText() == "CPF":

            self.documento.setPlaceholderText(
                "Digite o CPF"
            )

        else:

            self.documento.setPlaceholderText(
                "Digite o CNPJ"
            )

    # ==========================================
    # LIMPAR
    # ==========================================

    def limpar(self):

        self.nome.clear()
        self.documento.clear()
        self.email.clear()
        self.celular.clear()
        self.cep.clear()
        self.logradouro.clear()
        self.numero.clear()
        self.complemento.clear()
        self.bairro.clear()
        self.cidade.clear()

        self.tipo_documento.setCurrentIndex(0)
        self.estado.setCurrentIndex(0)

        QMessageBox.information(
            self,
            "Limpar",
            "Campos limpos com sucesso!"
        )

    # ==========================================
    # VALIDAR CPF
    # ==========================================

    def validar_cpf(self, cpf):

        cpf = re.sub(
            r"\D",
            "",
            cpf
        )

        if len(cpf) != 11:
            return False

        if cpf == cpf[0] * 11:
            return False

        soma = 0

        for i in range(9):
            soma += (
                int(cpf[i]) * (10 - i)
            )

        resto = (
            soma * 10
        ) % 11

        if resto == 10:
            resto = 0

        if resto != int(cpf[9]):
            return False

        soma = 0

        for i in range(10):
            soma += (
                int(cpf[i]) * (11 - i)
            )

        resto = (
            soma * 10
        ) % 11

        if resto == 10:
            resto = 0

        if resto != int(cpf[10]):
            return False

        return True

    # ==========================================
    # VALIDAR CNPJ
    # ==========================================

    def validar_cnpj(self, cnpj):

        cnpj = re.sub(
            r"\D",
            "",
            cnpj
        )

        if len(cnpj) != 14:
            return False

        if cnpj == cnpj[0] * 14:
            return False

        pesos1 = [
            5, 4, 3, 2,
            9, 8, 7, 6,
            5, 4, 3, 2
        ]

        soma = 0

        for i in range(12):

            soma += (
                int(cnpj[i]) *
                pesos1[i]
            )

        resto = soma % 11

        if resto < 2:
            digito1 = 0
        else:
            digito1 = 11 - resto

        if digito1 != int(cnpj[12]):
            return False

        pesos2 = [
            6, 5, 4, 3, 2,
            9, 8, 7, 6, 5,
            4, 3, 2
        ]

        soma = 0

        for i in range(13):

            soma += (
                int(cnpj[i]) *
                pesos2[i]
            )

        resto = soma % 11

        if resto < 2:
            digito2 = 0
        else:
            digito2 = 11 - resto

        if digito2 != int(cnpj[13]):
            return False

        return True

    # ==========================================
    # VALIDAR E-MAIL
    # ==========================================

    def validar_email(self, email):

        padrao = (
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        )

        return re.match(
            padrao,
            email
        ) is not None

    # ==========================================
    # VALIDAR CELULAR
    # ==========================================

    def validar_celular(self, celular):

        celular = re.sub(
            r"\D",
            "",
            celular
        )

        return len(celular) in (10, 11)

    # ==========================================
    # VALIDAR CEP
    # ==========================================

    def validar_cep(self, cep):

        cep = re.sub(
            r"\D",
            "",
            cep
        )

        return len(cep) == 8

    # ==========================================
    # VALIDAR FORMULÁRIO
    # ==========================================

    def validar_formulario(self):

        nome = self.nome.text().strip()

        documento = self.documento.text().strip()

        email = self.email.text().strip()

        celular = self.celular.text().strip()

        cep = self.cep.text().strip()

        logradouro = self.logradouro.text().strip()

        numero = self.numero.text().strip()

        bairro = self.bairro.text().strip()

        cidade = self.cidade.text().strip()

        # Nome
        if not nome:

            QMessageBox.warning(
                self,
                "Erro",
                "Digite o nome completo."
            )

            self.nome.setFocus()

            return False

        # Documento
        if self.tipo_documento.currentText() == "CPF":

            if not self.validar_cpf(documento):

                QMessageBox.warning(
                    self,
                    "Erro",
                    "Digite um CPF válido."
                )

                self.documento.setFocus()

                return False

        else:

            if not self.validar_cnpj(documento):

                QMessageBox.warning(
                    self,
                    "Erro",
                    "Digite um CNPJ válido."
                )

                self.documento.setFocus()

                return False

        # E-mail
        if not self.validar_email(email):

            QMessageBox.warning(
                self,
                "Erro",
                "Digite um e-mail válido."
            )

            self.email.setFocus()

            return False

        # Celular
        if not self.validar_celular(celular):

            QMessageBox.warning(
                self,
                "Erro",
                "Digite um celular válido."
            )

            self.celular.setFocus()

            return False

        # CEP
        if not self.validar_cep(cep):

            QMessageBox.warning(
                self,
                "Erro",
                "Digite um CEP válido."
            )

            self.cep.setFocus()

            return False

        # Logradouro
        if not logradouro:

            QMessageBox.warning(
                self,
                "Erro",
                "Informe o logradouro."
            )

            self.logradouro.setFocus()

            return False

        # Número
        if not numero:

            QMessageBox.warning(
                self,
                "Erro",
                "Informe o número."
            )

            self.numero.setFocus()

            return False

        # Bairro
        if not bairro:

            QMessageBox.warning(
                self,
                "Erro",
                "Informe o bairro."
            )

            self.bairro.setFocus()

            return False

        # Cidade
        if not cidade:

            QMessageBox.warning(
                self,
                "Erro",
                "Informe a cidade."
            )

            self.cidade.setFocus()

            return False

        # Estado
        if self.estado.currentText() == "Selecione":

            QMessageBox.warning(
                self,
                "Erro",
                "Selecione o estado."
            )

            self.estado.setFocus()

            return False

        return True

    # ==========================================
    # CONSULTAR CEP
    # ==========================================

    def consultar_cep(self):

        cep = re.sub(
            r"\D",
            "",
            self.cep.text()
        )

        if len(cep) != 8:

            QMessageBox.warning(
                self,
                "CEP inválido",
                "Digite um CEP com 8 números."
            )

            self.cep.setFocus()

            return

        try:

            url = (
                f"https://viacep.com.br/ws/"
                f"{cep}/json/"
            )

            resposta = urlopen(
                url,
                timeout=10
            )

            dados = json.loads(
                resposta.read().decode(
                    "utf-8"
                )
            )

            if dados.get("erro"):

                QMessageBox.warning(
                    self,
                    "CEP não encontrado",
                    "O CEP informado não foi encontrado."
                )

                return

            self.preencher_endereco(
                dados
            )

        except HTTPError:

            QMessageBox.critical(
                self,
                "Erro",
                "O serviço de CEP apresentou um erro."
            )

        except URLError:

            QMessageBox.critical(
                self,
                "Erro de conexão",
                "Não foi possível consultar o CEP.\n\n"
                "Verifique sua conexão com a internet."
            )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                f"Erro ao consultar o CEP:\n\n{erro}"
            )

    # ==========================================
    # PREENCHER ENDEREÇO
    # ==========================================

    def preencher_endereco(self, dados):

        self.logradouro.setText(
            dados.get(
                "logradouro",
                ""
            )
        )

        self.bairro.setText(
            dados.get(
                "bairro",
                ""
            )
        )

        self.cidade.setText(
            dados.get(
                "localidade",
                ""
            )
        )

        uf = dados.get(
            "uf",
            ""
        )

        for i in range(
            self.estado.count()
        ):

            if self.estado.itemText(
                i
            ).startswith(
                uf + " - "
            ):

                self.estado.setCurrentIndex(
                    i
                )

                break

        QMessageBox.information(
            self,
            "CEP encontrado",
            "Endereço preenchido automaticamente!"
        )

        self.numero.setFocus()

    # ==========================================
    # SALVAR
    # ==========================================

    def salvar(self):

        if not self.validar_formulario():
            return

        nome = self.nome.text().strip()

        tipo_documento = (
            self.tipo_documento.currentText()
        )

        documento = re.sub(
            r"\D",
            "",
            self.documento.text()
        )

        email = self.email.text().strip()

        celular = re.sub(
            r"\D",
            "",
            self.celular.text()
        )

        cep = re.sub(
            r"\D",
            "",
            self.cep.text()
        )

        logradouro = (
            self.logradouro.text().strip()
        )

        numero = self.numero.text().strip()

        complemento = (
            self.complemento.text().strip()
        )

        bairro = self.bairro.text().strip()

        cidade = self.cidade.text().strip()

        estado = self.estado.currentText()

        try:

            conexao = conectar_pessoas()

            cursor = conexao.cursor()

            # ==========================================
            # VERIFICA DOCUMENTO DUPLICADO
            # ==========================================

            cursor.execute("""
                SELECT id
                FROM pessoas
                WHERE documento = ?
            """, (documento,))

            existente = cursor.fetchone()

            if existente:

                conexao.close()

                QMessageBox.warning(
                    self,
                    "Documento já cadastrado",
                    f"Este {tipo_documento} "
                    "já está cadastrado."
                )

                return

            # ==========================================
            # INSERIR
            # ==========================================

            cursor.execute("""
                INSERT INTO pessoas (
                    nome_completo,
                    tipo_documento,
                    documento,
                    email,
                    celular,
                    cep,
                    logradouro,
                    numero,
                    complemento,
                    bairro,
                    cidade,
                    estado
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                nome,
                tipo_documento,
                documento,
                email,
                celular,
                cep,
                logradouro,
                numero,
                complemento,
                bairro,
                cidade,
                estado
            ))

            conexao.commit()

            conexao.close()

            QMessageBox.information(
                self,
                "Sucesso",
                "Pessoa cadastrada com sucesso!"
            )

            self.limpar_silencioso()

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível salvar o cadastro.\n\n"
                f"Erro: {erro}"
            )

    # ==========================================
    # LIMPAR SEM MENSAGEM
    # ==========================================

    def limpar_silencioso(self):

        self.nome.clear()
        self.documento.clear()
        self.email.clear()
        self.celular.clear()
        self.cep.clear()
        self.logradouro.clear()
        self.numero.clear()
        self.complemento.clear()
        self.bairro.clear()
        self.cidade.clear()

        self.tipo_documento.setCurrentIndex(
            0
        )

        self.estado.setCurrentIndex(
            0
        )


# ==========================================
# INICIAR PROGRAMA
# ==========================================

if __name__ == "__main__":

    # Cria/verifica os dois bancos
    criar_banco()

    app = QApplication(sys.argv)

    janela = CadastroPessoa()

    janela.show()

    sys.exit(app.exec())