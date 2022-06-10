import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split


class BTCDataset:
    def __init__(self, csv_file, features, response, history_length, train_ratio):
        self.df = pd.read_csv(csv_file)
        self.features = features
        self.response = response
        self.lookback_step = history_length
        self.train_ratio = train_ratio

    def prepare_train_test_ds(self, scaler):
        variables = scaler.fit_transform(self.df[self.features])
        response = scaler.fit_transform(self.df[[self.response]].values)
        X, y = [], []

        for i in range(self.lookback_step, len(self.df)):
            X.append(variables[i - self.lookback_step:i, :])
            y.append(response[i])

        X_train, X_test, y_train, y_test = train_test_split(np.array(X), np.array(y),
                                                            train_size=self.train_ratio, shuffle=False)

        return torch.from_numpy(X_train).float(), torch.from_numpy(y_train).float(), \
               torch.from_numpy(X_test).float(), torch.from_numpy(y_test).float()
