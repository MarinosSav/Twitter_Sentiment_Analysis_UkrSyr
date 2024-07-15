import pandas as pd
import time
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pattern.en import sentiment

def sentiment_analysis(dataset):

    sid = SentimentIntensityAnalyzer()
    polarities = []
    #sentiments = []
    for idx, tweet in enumerate(dataset[2]):
        if idx % 100000 == 0:
            print(idx, '/', dataset.shape[0])
        polarities.append(sid.polarity_scores(tweet)['compound'])
        #sentiments.append(sentiment(tweet)[0])

    dataset['polarity'] = polarities

    return dataset


def main():
    tic = time.perf_counter()

    df_syr = pd.read_csv("New/combine_syr_extra.csv", header=None)
    df_ukr = pd.read_csv("New/combine_ukr_extra.csv", header=None)

    df_syr = sentiment_analysis(df_syr)
    df_ukr = sentiment_analysis(df_ukr)

    df_syr.to_csv("New/combine_syr_extra.csv", index=False)
    df_ukr.to_csv("New/combine_ukr_extra.csv", index=False)


    print("Time taken:", time.perf_counter() - tic)


if __name__ == "__main__":
    main()
