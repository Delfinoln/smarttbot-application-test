# smarttbot-application-test
 This repository is destined to solve smarttbot's application test
# Considerações Gerais
## Solução
1. A solução pode ser dividida conforme o diagrama a seguir:
![smarttbot-application-test-diagram](https://user-images.githubusercontent.com/28309647/120120667-2f126080-c175-11eb-954f-3c8217d81201.png)

* Source:

Nossa fonte de dados é um websocket API da Poloniex. Através dela recebemos os seguinte dados:  currency pair id, last trade price, lowest ask, highest bid, percent change in last 24 hours, base currency volume in last 24 hours, quote currency volume in last 24 hours, is frozen, highest trade price in last 24 hours, lowest trade price in last 24 hours, post only e maintenance mode.

* Batch-layer:

Dentro do Batch-layer temos um container rodando uma aplicação responsável pela extração dos dados através da API da Poloniex, um Bucket (smarttbotrawzone), rodando em um container com MinIO, responsável pelo armazenamento do dado bruto (raw data) e um terceiro container rodando uma aplicação responsável pelo processamento do dado bruto e carga em um segundo Bucket (smarttbottrustedzone).

* Serving-layer:

Dentro do Serving-layer temos o Bucket smarttbottrustedzone, no qual serão armazenados os dados das candles do BTC e do ETH nos tempos de 1 minuto e 5 minutos. Este bucket roda no mesmo container MinIO do Bucket destinado ao dado bruto.


2. Foi adotado o encapsulamento em Docker Compose para facilitar a reprodução do projeto.

## Como utilizar
Para reproduzir a aplicação, utilize o ```Makefile```
```
cd src      # diretório onde está o Makefile
make all    # build da imagem e inicialização do docker compose
```
## Resultado
A aplicação gera 5 arquivos .csv:
* fullrawdata.csv: arquivo .csv que contém o dado bruto recebido da API da Poloniex sobre o BTC (id 121) e o ETH (id 149)
* btc_1min.csv: arquivo .csv com os dados de cada candle do Bitcoin no período de 1 minuto;
* btc_5min.csv: arquivo .csv com os dados de cada candle do Bitcoin no período de 5 minuto;
* eth_1min.csv: arquivo .csv com os dados de cada candle do Etherium no período de 1 minuto;
* eth_5min.csv: arquivo .csv com os dados de cada candle do Etherium no período de 5 minuto.

Os arquivos de dados, bruto ou processados, estão dentro dos Buckets que podem ser encontrados no diretório ```/src/minio_data/```, diretório compartilhado com o Container por meio de volumes. O Bucket smarttbotrawzone é destinado ao arquivo bruto, enquanto o Bucket smarttbottrustedzone é destinado aos dados processados.

## Tecnologias
* Python
* API
* Docker Compose
* MinIO: minIO é um servidor de armazenamento de objetos, compatível com o armazenamento S3. MinIO pode ser usado para construir infraestruturas de alta performance para machine learning, analytics ou aplicações com Bigdata
