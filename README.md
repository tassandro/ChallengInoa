# Desafio Inoa
## Descrição do projeto

O projeto foi desenvolvido como parte do desafio técnico da empresa [Inoa Sistemas](https://www.inoa.com.br/). O desafio
consiste no desenvolvimento de um sistema utilizando Python com Django.

O objetivo do sistema é auxiliar um investidor nas suas decisões de comprar/vender ativos. Para tal, o sistema deve registrar periodicamente a cotação atual de ativos da B3 e também avisar, via e-mail, caso haja oportunidade de negociação.


**Os seguintes requisitos funcionais são necessários:**

* Expor uma interface web para permitir que o usuário configure:
1. os ativos da B3 a serem monitorados;
2. os parâmetros de túnel de preço (www.b3.com.br/pt_br/solucoes/plataformas/puma-trading-system/para-participantes-e-traders/regras-e-parametros-de-negociacao/tuneis-de-negociacao) de cada ativo;
3. a periodicidade da checagem (em minutos) de cada ativo.
 
* O sistema deve obter e armazenar as cotações dos ativos cadastrados de alguma fonte pública qualquer, respeitando a periodicidade configurada por ativo.

* A interface web deve permitir consultar os preços armazenados dos ativos cadastrados.

* Enviar e-mail para o investidor sugerindo a compra sempre que o preço de um ativo monitorado cruzar o seu limite inferior do túnel, e sugerindo a venda sempre que o preço de um ativo monitorado cruzar o seu limite superior do túnel

## Requisitos

O projeto foi desenvolvido utilizando a versão **3.10** do Python.

Para rodar o projeto, siga os seguintes passos:

1. **Clonar o repositório**

```shell
git clone https://github.com/AdaltonF/Desafio-Inoa.git
```

2. **Criar um ambiente virtual com as bibliotecas utilizadas**

```shell
python -m venv venv
```
Para ativar o ambiente virtual no Windows:
```shell
venv\Scripts\activate
```
3. **Instalar bibliotecas do projeto**

```shell
pip install -r requirements.txt
```

4. **Configurar variáveis de ambiente**

Crie um arquivo `.env` e defina as seguintes variáveis:
```
EMAIL_HOST_USER=seu_email@email.com
EMAIL_HOST_PASSWORD=sua_senha
API_KEY=chave_da_api_BRAPI
```
* Caso utilize algum servido de email diferente do Gmail, é necessário alterar o `EMAIL_HOST` no arquivo `settings.py`.
* Para o Gmail, é possível criar uma senha de aplicação. Informaçõe [aqui](https://support.google.com/mail/answer/185833?hl=pt-BR)
* Obtenha um chave da API gratuitamente pode meio do site: https://brapi.dev/

5. **Execute as migrações do banco de dados**
```shell
python manage.py migrate
```
6. **Inicie o servidor**
```shell
python manage.py runserver
```

