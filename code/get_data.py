import requests
import pandas as pd
import json
import time
import datetime as dt

bearer_token = "AAAAAAAAAAAAAAAAAAAAACvwdQEAAAAACTZgJ8dF%2B7AIpO3%2FYBdUpwNcXZk%3DahAqAN1ZrPzI92KutplISybnbYxXCMjTQofOf2gjRawX6QGVST"
max_tweets = 2000000
tweets_per_request = 500


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        if response.status_code == 429:
            return 1
        raise Exception(response.status_code, response.text)
    return response.json()


def join_dataframes(df_data, df_users, df_tweets):

    ref_id = []
    for i, ref_tweet in enumerate(df_data["referenced_tweets"]):
        if type(ref_tweet) is list:
            ref_id.append(ref_tweet[0]["id"])
        else:
            ref_id.append(df_data["tweet_id"][i])
    df_data["referenced_tweets"] = ref_id

    df_data_users = pd.merge(df_data, df_users, left_on="author_id", right_on="id")

    df = pd.merge(df_data_users, df_tweets, left_on="referenced_tweets", right_on="id")
    df = df[["created_at_x", "text_y", "location"]]
    df.rename(columns={"text_y": "text", "created_at_x": "date"}, inplace=True)

    return df


def trim_dates(df):

    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%dT%H:%M:%S.%f")
    df['date'] = df['date'].dt.strftime('%d-%m-%Y')

    return df


def make_dataframe(json_response):

    df_data = pd.DataFrame(json_response["data"])
    df_data.rename(columns={'id': 'tweet_id'}, inplace=True)
    df_users = pd.DataFrame(json_response["includes"]["users"])
    df_tweets = pd.DataFrame(json_response["includes"]["tweets"])

    df = join_dataframes(df_data, df_users, df_tweets)
    df = trim_dates(df)

    return df


def main(start_time, end_time):
    count_pulled = 0
    next_token = None
    endpoint = "https://api.twitter.com/2/tweets/search/all"
    #refugee OR refugees OR migrant OR migrants OR
    base_query = '(immigrant OR immigrants OR immigration OR displaced OR stateless OR "asylum seeker" OR ' \
                 '"asylum seekers" OR "displaced person" OR "stateless person") -(expat OR expats) lang:en '
    query_ukr = '-(syria OR syrian) (ukraine OR ukrainian)'
    query_syr = '(syria OR syrian) -(ukraine OR ukrainian)'

    while True:
        query_params = {"query": base_query + query_ukr,
                        "max_results": tweets_per_request,
                        "expansions": "author_id,referenced_tweets.id",
                        "start_time": start_time,
                        "end_time": end_time,
                        "tweet.fields": "created_at",
                        "user.fields": "location",
                        "next_token": next_token}
        json_response = connect_to_endpoint(endpoint, query_params)
        if json_response == 1:
            time.sleep(900)
            continue

        print(base_query+query_syr)
        next_token = json_response["meta"]["next_token"]

        df = make_dataframe(json_response)
        print(df["date"].iloc[-1])

        if len(df.index) == 0:
            return
        count_pulled += len(df.index)
        if count_pulled > max_tweets:
            return

        df.to_csv("data.csv", mode='a', header=False, encoding='utf-8')
        print("Tweets requested:", count_pulled)
        time.sleep(1)


if __name__ == "__main__":

    start_time = "2022-02-26T00:00:00Z"
    end_time = "2022-03-07T23:59:59Z"

    main(start_time, end_time)
    print("Done")
