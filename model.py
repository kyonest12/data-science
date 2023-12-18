import csv
import json

import joblib
import os

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import xgboost as xgb


class Model:
    def __init__(self, model_path):
        with open("scale.json", 'r') as json_file:
            self.scale_data = json.load(json_file)
        if model_path == "":
            self.model = xgb.XGBClassifier(objective='binary:logistic', random_state=42)
        else:
            try:
                self.model = joblib.load(model_path)
            except FileNotFoundError:
                self.model = xgb.XGBClassifier(objective='binary:logistic', random_state=42)

    def train_model(self, file_path):
        data = pd.read_csv(file_path)

        data['datetime'] = pd.to_datetime(data['datetime'])
        data['Year'] = data['datetime'].dt.year
        data['Month'] = data['datetime'].dt.month
        data['Day'] = data['datetime'].dt.day
        data['Hour'] = data['datetime'].dt.hour
        columns_to_drop = ['datetime', 'preciptype', 'solarradiation', 'uvindex']
        X = data.drop(['labels'] + columns_to_drop, axis=1)
        y = data['labels']
        X['sealevelpressure'] /= 1000
        X['humidity'] /= 100
        X['winddir'] = X['winddir'].apply(lambda x: 0.25 * (x / 90) if 0 <= x <= 90 else
        0.25 + 0.25 * ((x - 90) / 90) if 90 < x <= 180 else
        0.5 + 0.25 * ((x - 180) / 90) if 180 < x <= 270 else
        0.75 + 0.25 * ((x - 270) / 90) if 270 < x <= 360 else x)
        X['cloudcover'] /= 100
        X['temp'] = (X['temp'] - self.scale_data['min_values']['temp']) / (
                    self.scale_data['max_values']['temp'] - self.scale_data['min_values']['temp'])
        X['dew'] = (X['dew'] - self.scale_data['min_values']['dew']) / (
                    self.scale_data['max_values']['dew'] - self.scale_data['min_values']['dew'])
        X['windgust'] = (X['windgust'] - self.scale_data['min_values']['windgust']) / (
                    self.scale_data['max_values']['windgust'] - self.scale_data['min_values']['windgust'])
        X['windspeed'] = (X['windspeed'] - self.scale_data['min_values']['windspeed']) / (
                    self.scale_data['max_values']['windspeed'] - self.scale_data['min_values']['windspeed'])
        X['solarenergy'] = (X['solarenergy'] - self.scale_data['min_values']['solarenergy']) / (
                    self.scale_data['max_values']['solarenergy'] - self.scale_data['min_values']['solarenergy'])

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Accuracy: {accuracy}')

        current_directory = os.getcwd()
        model_path = os.path.join(current_directory, "model.pkl")
        joblib.dump(self.model, model_path)

    def predict(self, array):
        return model.predict(array)


def read_csv_and_generate_scale_json(csv_file_path, scale_json_file_path):
    with open(csv_file_path, 'r') as csv_file:

        csv_reader = csv.DictReader(csv_file)
        min_values = {'temp': float('inf'), 'dew': float('inf'), 'windgust': float('inf'), 'windspeed': float('inf'),
                      'solarenergy': float('inf')}
        max_values = {'temp': float('-inf'), 'dew': float('-inf'), 'windgust': float('-inf'),
                      'windspeed': float('-inf'), 'solarenergy': float('-inf')}

        for row in csv_reader:
            for field in ['temp', 'dew', 'windgust', 'windspeed', 'solarenergy']:
                value = float(row[field])
                min_values[field] = min(min_values[field], value)
                max_values[field] = max(max_values[field], value)

    # Tạo đối tượng scale từ giá trị min và max
    scale = {'min_values': min_values, 'max_values': max_values}

    # Lưu đối tượng scale vào file JSON
    with open(scale_json_file_path, 'w') as json_file:
        json.dump(scale, json_file, indent=2)


csv_file_path = 'data.csv'
scale_json_file_path = 'scale.json'

read_csv_and_generate_scale_json(csv_file_path, scale_json_file_path)

model = Model("model.pkl")
model.train_model("data.csv")
