import pandas as pd


def remove(file_path):
    df = pd.read_csv(file_path)

    columns_to_remove = ['name', 'feelslike', 'precip', 'precipprob', 'snow', 'snowdepth', 'conditions', 'icon',
                        'severerisk']
    df = df.drop(columns=columns_to_remove)

    df.to_csv(file_path, index=False)


def add_labels(input_file, output_file):
    df = pd.read_csv(input_file)

    df['labels'] = df['preciptype'].shift(-1).apply(lambda x: 1 if x == 'rain' else 0)
    df = df.drop(df.index[-1])
    df.to_csv(output_file, index=False)


def process_csv(file_path):
    df = pd.read_csv(file_path)

    df['windgust'].fillna(df['windspeed'], inplace=True)
    columns_to_fill = ['solarradiation', 'solarenergy', 'uvindex']

    df[columns_to_fill] = df[columns_to_fill].fillna(0)
    df['sealevelpressure'] /= 1000

    df.to_csv(file_path, index=False)


remove("dataCurrent.csv")
add_labels("dataCurrent.csv", "dataCurrent.csv")
process_csv("dataCurrent.csv")
