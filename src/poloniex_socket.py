import json
import websocket
import time
import pandas as pd
from minio import Minio

SOCKET = "wss://api2.poloniex.com"

PARAMETERS = {
    "command": "subscribe",
    "channel": 1002
}

cripto_list = []
usdt_btc_oneminute = []
timestamps = []
rawdata_dict = {}
fullrawdata_header = ["currency pair id", "last trade price", "lowest ask", "highest bid",
                      "percent change in last 24 hours", "base currency volume in last 24 hours",
                      "quote currency volume in last 24 hours", "is frozen", "highest trade price in last 24 hours",
                      "lowest trade price in last 24 hours", "post only", "maintenance mode", "timestamp"]
fullrawdata_dict = {key: [] for key in fullrawdata_header}
counter = 1


def on_open(ws):
    print('opened connection')
    ws.send(json.dumps(PARAMETERS, indent=3))
    print("Command sent")


def on_close(ws):
    print("closed connection. Trying to reconnect")
    ws = websocket.WebSocketApp(SOCKET,
                                on_open=on_open,
                                on_close=on_close,
                                on_message=on_message,
                                on_error=on_error)
    ws.run_forever()


def on_ping(ws, message):
    print(f"Got a ping!")


def on_pong(ws, message):
    global counter
    print(f"Got a pong: {counter}")
    counter += 1


def on_message(ws, message):
    global cripto_list
    global t0
    global counter

    cripto_list = message.replace("[", "").replace("]", "").replace('"', "").split(",")

    if len(cripto_list) > 2:
        t1 = time.time() - t0

        # appending field timestamp in cripto_list
        cripto_list.append(time.time())

        # Selecting USDT_BTC, id 121, and USDT_ETH, id 149
        if int(cripto_list[2]) == 121 or int(cripto_list[2]) == 149:
            for key in fullrawdata_header:
                fullrawdata_dict[key].append(cripto_list[fullrawdata_header.index(key) + 2])

            # if t1 <= 60:
            #     usdt_btc_oneminute.append(float(cripto_list[3]))
            #     timestamps.append(time.time())
            #     rawdata_dict["price"] = usdt_btc_oneminute
            #     rawdata_dict["timestamps"] = timestamps
            #     df = pd.DataFrame(rawdata_dict, columns=['price', 'timestamps'])
            #     df.to_csv('rawdata.csv', index=False)
            if t1 > 59:
                # upload_files("rawdata.csv", "smarttbots3bucket")
                print("Uploading files")
                df2 = pd.DataFrame(fullrawdata_dict, columns=fullrawdata_header)
                df2.to_csv('fullrawdata.csv', index=False)
                client.fput_object("smarttbotrawzone", "fullrawdata.csv", "fullrawdata.csv")
                t0 = time.time()


def on_error(ws, error):
    print(error)


if __name__ == "__main__":
    time.sleep(10)

    client = Minio(
        "minio:9000",
        access_key="Q3AM3UQ867SPQQA43P2F",
        secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
        secure=False
    )

    # Make 'raw-zone' bucket if not exist.
    found = client.bucket_exists("smarttbotrawzone")
    if not found:
        client.make_bucket("smarttbotrawzone")
        print("Bucket created")
    else:
        print("Bucket 'smarttbotrawzone' already exists")

    t0 = time.time()
    ws = websocket.WebSocketApp(SOCKET,
                                on_open=on_open,
                                on_close=on_close,
                                on_message=on_message,
                                on_error=on_error,
                                on_ping=on_ping,
                                on_pong=on_pong)
    ws.run_forever(ping_interval=5)