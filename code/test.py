import pandas as pd
from datetime import timedelta
import numpy as np
#import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pattern.en import sentiment
from scipy import stats


def pattern_analyze(df):

    pattern = []
    for tweet in df['text']:
        pattern.append(sentiment(tweet)[0])
    df['pattern_score'] = pattern

    return df


def main():

    df_syr = pd.read_csv("data_syr_full.csv")
    df_ukr = pd.read_csv("data_syr_full.csv")

    #
    df.to_csv("ManualAnnotation/annotated_sample.csv", index=False)


if __name__ == "__main__":
    main()
