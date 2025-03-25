# Desafio Inoa

## Descrição do projeto

O projeto foi desenvolvido como parte do desafio técnico da empresa [Inoa Sistemas](https://www.inoa.com.br/). O desafio consiste no desenvolvimento de um sistema utilizando **Python com Django**.

O objetivo do sistema é auxiliar um investidor na tomada de decisões de compra e venda de ativos. Para isso, o sistema registra periodicamente a cotação atual de ativos da B3 e notifica o investidor por e-mail sempre que um ativo atinge o limite inferior (sinalizando uma oportunidade de compra) ou o limite superior (sinalizando uma oportunidade de venda).

---

## Funcionalidades

O sistema implementa os seguintes requisitos funcionais:

- Interface web para permitir que o usuário:
  1. Configure os ativos da B3 a serem monitorados;
  2. Defina os parâmetros de túnel de preço ([mais informações sobre os túneis de negociação da B3](https://www.b3.com.br/pt_br/solucoes/plataformas/puma-trading-system/para-participantes-e-traders/regras-e-parametros-de-negociacao/tuneis-de-negociacao));
  3. Escolha a periodicidade da checagem de cada ativo (em minutos).

- O sistema obtém e armazena as cotações dos ativos cadastrados utilizando a API pública [BRAPI](https://brapi.dev/), respeitando a periodicidade definida para cada ativo.

- Interface web para consulta dos preços armazenados dos ativos cadastrados.

- Envio automático de e-mails:
  - Alerta de compra quando o preço do ativo atinge ou cruza o limite inferior configurado.
  - Alerta de venda quando o preço do ativo atinge ou cruza o limite superior configurado.

---

Para rodar o projeto localmente, siga os passos abaixo:

## Clonar o repositório

```
git clone https://github.com/tassandro/ChallengInoa.git
cd Desafio-Inoa
```


## Criar um ambiente virtual e instalar as dependências
Criação do ambiente virtual:

```
python -m venv venv
Ativação do ambiente virtual:
```

Windows:

```
venv\Scripts\activate
```

Linux/macOS:

```
source venv/bin/activate
```

Instalação das bibliotecas necessárias:

```
pip install -r requirements.txt
```

## Configuração das variáveis de ambiente
Crie um arquivo .env na raiz do projeto e adicione as seguintes variáveis:


EMAIL_HOST_USER=seu_email@email.com
EMAIL_HOST_PASSWORD=sua_senha
API_KEY=chave_da_api_BRAPI
Caso utilize um serviço de e-mail diferente do Gmail, será necessário configurar o EMAIL_HOST no settings.py.

Se estiver usando Gmail, é necessário criar uma senha de aplicativo.

Obtenha uma chave gratuita da API BRAPI no site da [BRAPI](https://brapi.dev/).

## Configuração do banco de dados

Aplique as migrações do banco de dados:

```
python manage.py migrate
```

## Execução do servidor Django
Para rodar o servidor web:

```
python manage.py runserver
```
---

# Uso do Sistema

## Cadastro de Ativos
1. Acesse a interface web.
2. Cadastre os ativos da B3 que deseja monitorar.
3. Configure os limites de preço e a periodicidade das verificações.

## Consulta de Cotações
- O histórico de preços dos ativos cadastrados pode ser consultado na interface web.

## Monitoramento e Envio de Alertas
- O sistema verifica periodicamente as cotações e envia e-mails caso um ativo atinja os limites configurados.

---

# Problemas Enfrentados e Melhorias Futuras

## Dificuldades Encontradas

### 1. **Autenticação no Envio de E-mails**
- Inicialmente, houve problemas com a autenticação SMTP ao tentar enviar e-mails via Gmail.
- **Solução:** Utilização de uma senha de aplicativo.

### 2. **Persistência das Tarefas Agendadas**
- O agendador APScheduler foi configurado para armazenar as tarefas no banco de dados. No entanto, ao reiniciar o servidor, algumas tarefas poderiam ser executadas mais de uma vez simultaneamente, gerando registros duplicados.

### 3. **Execução Contínua do Monitoramento**
- O sistema de monitoramento depende da execução contínua do servidor Django.

---




