import os

import torch
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler

from config import DATA_DIR
from crawler import get_records
from model.dataset import BTCDataset
from model.ltsm import BtcLSTM
from utils.api_caller import RecordType
from utils.data_utils import json_to_csv


def prepare_csv_file(record_type: RecordType):
    raw_file = os.path.join(DATA_DIR, f'raw_{record_type.name}.txt')
    csv_file = os.path.join(DATA_DIR, f'raw_{record_type.name}.csv')
    json_to_csv(raw_file, csv_file, 'timestr', 'time', 'open', 'close', 'low', 'high', 'volumefrom', 'volumeto')


def train_predictor():
    csv_file = os.path.join(DATA_DIR, f'raw_{RecordType.DAILY.name}.csv')
    scaler = MinMaxScaler(feature_range=(0, 1))
    features = ['open', 'close', 'low', 'high']
    ds_creator = BTCDataset(csv_file=csv_file, features=features, response='close',
                            history_length=30, train_ratio=0.8)
    X_train, y_train, X_test, y_test = ds_creator.prepare_train_test_ds(scaler)

    model = BtcLSTM(num_features=len(features), num_hidden=2, num_layers=1)
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(1, 2001):
        out = model(X_train)
        loss = criterion(out, y_train)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch % 100 == 0:
            print(f'Epoch {epoch}: {loss.item()}')

    torch.save(model, 'lstm_model')

    y_test_pred = model(X_test)
    y_test_pred = scaler.inverse_transform(y_test_pred.detach().numpy())
    y_test = scaler.inverse_transform(y_test.detach().numpy())

    # plot prediction vs real
    plt.plot(y_test, color='blue', label='true')
    plt.plot(y_test_pred, color='red', label='predict')
    plt.legend()
    plt.savefig('price_prediction_lstm.png', format='png')
    plt.show()


# 1st: crawl data from cryptocompare
# get_records(record_type=RecordType.DAILY)
# get_records(record_type=RecordType.HOURLY)

# 2nd: convert to csv file
# prepare_csv_file(RecordType.HOURLY)
# prepare_csv_file(RecordType.DAILY)

# 3rd: train a predictor to predict close price based on historic data
# train_predictor()
