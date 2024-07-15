import pandas as pd
from datetime import timedelta
import numpy as np
#import matplotlib.pyplot as plt


def trim_df(df):

    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%dT%H:%M:%S.%f")
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

    peak_date = df.groupby(['date']).count()['text'].idxmax()
    print("Peak date", peak_date)
    df = df[(df['date'] < peak_date + timedelta(30)) & (df['date'] > peak_date - timedelta(30))]

    return df


def main():
    df_syr = pd.read_csv("data_full_syr_sentiment.csv")
    print(df_syr.shape)
    df_ukr = pd.read_csv("data_full_ukr_sentiment.csv")
    print(df_ukr.shape)

    df_syr = trim_df(df_syr)
    df_ukr = trim_df(df_ukr)

    df_syr.to_csv("data_full_sry_sentiment_trimmed.csv", index=False)
    df_ukr.to_csv("data_full_ukr_sentiment_trimmed.csv", index=False)


if __name__ == "__main__":
    main()
