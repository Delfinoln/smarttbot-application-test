FROM python:3.8-slim-buster AS poloniex_socket

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 9001
CMD [ "python3", "poloniex_socket.py"]


FROM python:3.8-slim-buster as poloniex_enrich

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 9002
CMD [ "python3", "poloniex_enrich.py"]