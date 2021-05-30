# smarttbot-application-test
 This repository is destined to solve smarttbot's application test
# Considerações Gerais
## Solução
A solução pode ser dividida conforme o diagrama a seguir:
![smarttbot-application-test-diagram](https://user-images.githubusercontent.com/28309647/120120667-2f126080-c175-11eb-954f-3c8217d81201.png)
1. Source
Nossa fonte de dados é um websocket API da Poloniex. Através dela recebemos os seguinte dados:  currency pair id, last trade price, lowest ask, highest bid, percent change in last 24 hours, base currency volume in last 24 hours, quote currency volume in last 24 hours, is frozen, highest trade price in last 24 hours, lowest trade price in last 24 hours, post only e maintenance mode.
