import pandas as pd
import os

path = "/Users/marin/Desktop/twitterapi/New/"
starts_with = 'combine'

file_list = [path + f for f in os.listdir(path) if f.startswith(starts_with)]
df_list = []
for file in sorted(file_list):
    df = pd.read_csv(file)
    df.columns = ['date', 'text', 'location', 'polarity', 'country']
    df_list.append(df)
    print(df.shape)

csv_merged = pd.concat(df_list, ignore_index=True)
csv_merged.drop_duplicates()
csv_merged.sort_values(by=['date'], ascending=True)
csv_merged.to_csv(path + 'data_full_' + starts_with + '.csv', index=False)

print(csv_merged.shape)
print(csv_merged['date'].iat[0], csv_merged['date'].iat[-1])