# smarttbot-application-test
 This repository is destined to solve smarttbot's application test
# Considerações Gerais
## Solução
1. A solução pode ser dividida conforme o diagrama a seguir:
![smarttbot-application-test-diagram](https://user-images.githubusercontent.com/28309647/120120667-2f126080-c175-11eb-954f-3c8217d81201.png)

* Source:

Nossa fonte de dados é um websocket API da Poloniex. Através dela recebemos os seguinte dados:  currency pair id, last trade price, lowest ask, highest bid, percent change in last 24 hours, base currency volume in last 24 hours, quote currency volume in last 24 hours, is frozen, highest trade price in last 24 hours, lowest trade price in last 24 hours, post only e maintenance mode.

* Batch-layer:

Dentro do Batch-layer temos um container rodando uma aplicação responsável pela extração dos dados através da API da Poloniex, um Bucket (smarttbotrawzone), rodando em um container com minIO, responsável pelo armazenamento do dado bruto (raw data) e um terceiro container rodando uma aplicação responsável pelo processamento do dado bruto e carga em um segundo Bucket (smarttbottrustedzone).

* Serving-layer:

Dentro do Serving-layer temos o Bucket smarttbottrustedzone, no qual serão armazenados os dados das candles do BTC e do ETH nos tempos de 1 minuto e 5 minutos. Este bucket roda no mesmo container minIO do Bucket destinado ao dado bruto.


2. Foi adotado o encapsulamento em Docker Compose para facilitar a reprodução do projeto.
