import pandas as pd
from datetime import timedelta
import numpy as np
#import matplotlib.pyplot as plt


def main():
    df_syr = pd.read_csv("data_full_syr_sentiment_trimmed_europe.csv")
    df_ukr = pd.read_csv("data_full_ukr_sentiment_trimmed_europe.csv")

    df_syr_sample = df_syr['text'].sample(n=100, random_state=1)
    df_ukr_sample = df_ukr['text'].sample(n=100, random_state=1)

    df_syr_sample.to_csv("sample_syr.csv", index=False)
    df_ukr_sample.to_csv("sample_ukr.csv", index=False)


if __name__ == "__main__":
    main()
