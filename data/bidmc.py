import pandas as pd
import matplotlib.pyplot as plt

def get_bidmc_csv_data(url):

    # Import the csv from physionet
    df = pd.read_csv(url)

    # Strip the column names
    df.columns = df.columns.str.strip()
    df.drop('PULSE', axis=1, inplace=True)
    df.dropna(inplace=True)

    heart_rates = df['HR'].to_numpy()
    respiration = df['RESP'].to_numpy()
    spo2 = df['SpO2'].to_numpy()

    return heart_rates, respiration, spo2
