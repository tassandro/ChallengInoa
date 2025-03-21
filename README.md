# ChallengInoa

## Descrição do Projeto

O projeto **ChallengInoa** foi desenvolvido como parte do desafio técnico da empresa **Inoa Sistemas**. O objetivo deste sistema é auxiliar investidores nas suas decisões de compra e venda de ativos, utilizando Python e Django como principais tecnologias.

O sistema realiza o monitoramento contínuo de ativos da **B3**, registrando suas cotações periodicamente e enviando notificações por e-mail sempre que houver oportunidades de negociação. As funcionalidades incluem a configuração de ativos monitorados, parâmetros de negociação e a periodicidade de checagem.

## Funcionalidades

- **Configuração de Ativos**: O usuário pode configurar os ativos da B3 a serem monitorados, incluindo:
  - Definição dos ativos a serem monitorados.
  - Configuração dos parâmetros de túnel de preço para cada ativo, com base nas regras de negociação da B3. [Mais informações sobre os parâmetros de túnel](https://www.b3.com.br/pt_br/solucoes/plataformas/puma-trading-system/para-participantes-e-traders/regras-e-parametros-de-negociacao/tuneis-de-negociacao/).
  - Definição da periodicidade da checagem de cada ativo (em minutos).

- **Monitoramento de Preços**: O sistema coleta periodicamente as cotações dos ativos cadastrados de uma fonte pública confiável, respeitando os intervalos de tempo configurados.

- **Consulta de Preços**: A interface web permite que o usuário consulte os preços armazenados dos ativos monitorados.

- **Notificações por E-mail**: O sistema envia e-mails para o investidor nas seguintes condições:
  - **Sugestão de Compra**: Quando o preço de um ativo monitorado ultrapassar seu limite inferior do túnel de preço.
  - **Sugestão de Venda**: Quando o preço de um ativo monitorado ultrapassar seu limite superior do túnel de preço

