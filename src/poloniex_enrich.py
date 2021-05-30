import pandas as pd
import time
from minio import Minio


def process_data(cripto_data, candle_time):
    start_index = 0
    current_timestamp = 0
    current_high = 0
    current_low = 0
    current_open = 0
    current_close = 0
    last_price = 0

    date = []
    open_values = []
    high_values = []
    low_values = []
    close_values = []

    for index, row in cripto_data.iterrows():
        if index == start_index:
            current_timestamp = row["timestamp"]
            current_open = row["last trade price"]
            current_high = row['last trade price']
            current_low = row['last trade price']

        if row["timestamp"] - current_timestamp <= candle_time:
            if row["last trade price"] > current_high:
                current_high = row["last trade price"]
            if row["last trade price"] < current_low:
                current_low = row["last trade price"]
            last_price = row["last trade price"]

        else:
            current_close = last_price
            open_values.append(current_open)
            close_values.append(current_close)
            high_values.append(current_high)
            low_values.append(current_low)
            date.append(time.strftime('%Y-%m-%d %H:%M', time.localtime(current_timestamp)))

            current_timestamp = row['timestamp']
            current_open = row['last trade price']
            current_high = row['last trade price']
            current_low = row['last trade price']

        data_dict = {
            'Date': date,
            'Open Value': open_values,
            'Close Value': close_values,
            'High Value': high_values,
            'Low Value': low_values,
        }

    return data_dict


def get_data():
    return client.fget_object("smarttbotrawzone", "fullrawdata.csv", "fullrawdata.csv")


if __name__ == "__main__":
    header = ['Date', 'Open Value', 'Close Value', 'High Value', 'Low Value']

    time.sleep(10)

    client = Minio(
        "minio:9000",
        access_key="Q3AM3UQ867SPQQA43P2F",
        secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
        secure=False

    )

    # Make 'trusted-zone' bucket if not exist.
    found = client.bucket_exists("smarttbottrustedzone")
    if not found:
        client.make_bucket("smarttbottrustedzone")
    else:
        print("Bucket 'smarttbottrustedzone' already exists")

    while True:
        time.sleep(80)
        print("Getting data")
        get_data()
        df = pd.read_csv("fullrawdata.csv")
        print(df)

        # Selecting only BTC information, id 121
        btc_data = df.loc[df['currency pair id'] == 121]

        # Selecting 2 columns that matter
        btc_data = btc_data[['last trade price', 'timestamp']]

        # Selecting only ETH information, id 149
        eth_data = df.loc[df['currency pair id'] == 149]

        # Selecting 2 columns that matter
        eth_data = eth_data[['last trade price', 'timestamp']]

        btc_1min_dict = process_data(btc_data, 60)
        btc_1min_df = pd.DataFrame(btc_1min_dict, columns=header)
        btc_1min_csv = btc_1min_df.to_csv("btc_1min.csv", index=False)

        btc_5min_dict = process_data(btc_data, 300)
        btc_5min_df = pd.DataFrame(btc_5min_dict, columns=header)
        btc_5min_csv = btc_5min_df.to_csv("btc_5min.csv", index=False)

        eth_1min_dict = process_data(eth_data, 60)
        eth_1min_df = pd.DataFrame(eth_1min_dict, columns=header)
        eth_1min_csv = eth_1min_df.to_csv("eth_1min.csv", index=False)

        eth_5min_dict = process_data(eth_data, 300)
        eth_5min_df = pd.DataFrame(eth_5min_dict, columns=header)
        eth_5min_csv = eth_5min_df.to_csv("eth_5min.csv", index=False)

        client.fput_object("smarttbottrustedzone", "btc_1min.csv", "btc_1min.csv")
        client.fput_object("smarttbottrustedzone", "btc_5min.csv", "btc_5min.csv")
        client.fput_object("smarttbottrustedzone", "eth_1min.csv", "eth_1min.csv")
        client.fput_object("smarttbottrustedzone", "eth_5min.csv", "eth_5min.csv")
        print("files uploaded")