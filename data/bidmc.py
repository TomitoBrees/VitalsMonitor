import pandas as pd
import matplotlib.pyplot as plt

def get_bidmc_csv_data(n):
    if n <= 0 or n > 53:
        raise Exception("The file number should be between 0 and 53")

    if 0 < n < 10:
        file_n = "0" + str(n)
    else:
        file_n = str(n)

    df = pd.read_csv(f"https://www.physionet.org/files/bidmc/1.0.0/bidmc_csv/bidmc_{file_n}_Numerics.csv")

    # Strip the column names
    df.columns = df.columns.str.strip()
    df.drop('PULSE', axis=1, inplace=True)
    df.dropna(inplace=True)

    heart_rates = df['HR'].to_numpy()
    respiration = df['RESP'].to_numpy()
    spo2 = df['SpO2'].to_numpy()

    return heart_rates, respiration, spo2
