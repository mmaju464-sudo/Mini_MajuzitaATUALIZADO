ATV8 - Sistema de Cadastro de Pessoa
=====================================

DESCRIÇÃO
---------

Aplicação desktop desenvolvida em Python utilizando PySide6.

O sistema permite cadastrar pessoas, validar os dados informados,
consultar automaticamente o endereço através do CEP e armazenar
os dados em um banco de dados SQLite.


REQUISITOS
----------

- Python 3
- PySide6
- Conexão com a internet para consultar o CEP


INSTALAÇÃO
----------

Abra o terminal na pasta do projeto e execute:

pip install PySide6


COMO EXECUTAR
-------------

Execute o seguinte comando:

python cadastro.py


BANCO DE DADOS
--------------

O sistema utiliza SQLite.

O arquivo "pessoas.db" é criado automaticamente na primeira execução.

Não é necessário instalar um servidor de banco de dados.


FUNCIONALIDADES
---------------

- Cadastro de pessoa;
- Cadastro de CPF ou CNPJ;
- Validação de CPF;
- Validação de CNPJ;
- Validação de e-mail;
- Validação de celular;
- Validação de CEP;
- Consulta automática do endereço pelo CEP;
- Preenchimento automático de logradouro;
- Preenchimento automático de bairro;
- Preenchimento automático de cidade;
- Preenchimento automático de estado;
- Tratamento de CEP inexistente;
- Tratamento de problemas de conexão;
- Salvamento dos dados no banco SQLite;
- Limpeza do formulário;
- Mensagens de erro e sucesso.


ARQUIVOS
--------

banco.py
    Responsável pela conexão e criação do banco de dados.

cadastro.py
    Contém a interface gráfica, validações, consulta do CEP
    e cadastro das pessoas.

README.txt
    Contém as instruções de instalação e execução.


API
---

A consulta de endereço utiliza a API ViaCEP.

É necessária conexão com a internet para realizar a consulta.


CAMPOS OBRIGATÓRIOS
-------------------

Nome completo
CPF ou CNPJ
E-mail
Celular
CEP
Logradouro
Número
Bairro
Cidade
Estado

ATIVIDADE 9 - CRUD, FILTRO E PDF
================================

A continuação da Atividade 8 adiciona as operações CRUD para pessoas:

- CREATE: cadastro da pessoa no banco SQLite;
- READ: visualização das pessoas em uma tabela;
- UPDATE: edição dos dados cadastrados;
- DELETE: exclusão de uma pessoa.

Também foram adicionados:

- Campo de filtro para pesquisar pessoas;
- Tabela com os dados do banco;
- Botão para exportar a tabela para PDF;
- Menu principal para acessar as telas.

REQUISITOS DA ATIVIDADE 9
-------------------------

Instale as bibliotecas com:

pip install PySide6
pip install reportlab

COMO EXECUTAR
-------------

Para abrir o sistema completo:

python main.py

Para abrir somente o cadastro original da Atividade 8:

python cadastro.py

ARQUIVOS NOVOS
--------------

main.py
    Menu principal do sistema.

lista_pessoas.py
    Exibe as pessoas em tabela, realiza READ, filtro,
    DELETE e exportação para PDF.

editar_pessoa.py
    Realiza o UPDATE dos dados da pessoa diretamente no SQLite.

requirements.txt
    Bibliotecas necessárias para executar o sistema.
