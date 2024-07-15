import pandas as pd
import time
import re


def find_country(dataset):

    country_dict = {'Albania': ['Albania', 'Shqipëri', 'AL'],
                    'Andorra': ['Andorra', 'AD'],
                    'Armenia': ['Armenia', 'Hayastan', 'AM'],
                    'Austria': ['Austria', 'Österreich', 'AT', 'OE'],
                    'Azerbaijan': ['Azerbaijan', 'AZ'],
                    'Belarus': ['Belarus', 'BY'],
                    'Belgium': ['Belgium', 'België', 'Belgique', 'Belgien', 'BE'],
                    'Bosnia and Herzegovina': ['Bosnia', 'Herzegovina', 'BA'],
                    'Bulgaria': ['Bulgaria', 'BG'],
                    'Croatia': ['Croatia', 'Hrvatska', 'HR'],
                    'Cyprus': ['Cyprus', 'Kipros', 'CY'],
                    'Czech Republic': ['Czech', 'Czechia', 'CZ'],
                    'Denmark': ['Denmark', 'Dannmark', 'DK'],
                    'Estonia': ['Estonia', 'Eesti', 'EE'],
                    'Finland': ['Finland', 'Suomi', 'FI'],
                    'France': ['France', 'FR'],
                    'Georgia': ['Georgia', 'Sakartvelo', 'GE'],
                    'Germany': ['Germany', 'Deutschland', 'DE'],
                    'Greece': ['Greece', 'Hellas', 'Ellada', 'GR'],
                    'Hungary': ['Hungary', 'Magyarország', 'HU'],
                    'Iceland': ['Iceland', 'Ísland', 'IS'],
                    'United Kingdom': ['United', 'Kingdom', 'Britain', 'England', 'Scotland', 'Wales', 'Northern', 'UK'],
                    'Ireland': ['Ireland', 'Éire', 'IE'],
                    'Italy': ['Italy', 'Italia', 'IT'],
                    'Kazakhstan': ['Kazakhstan', 'KZ'],
                    'Latvia': ['Latvia', 'Latvijas', 'LV'],
                    'Liechtenstein': ['Liechtenstein', 'LI'],
                    'Lithuania': ['Lithuania', 'Lietuva', 'LT'],
                    'Luxembourg': ['Luxembourg', 'Lëtzebuerg', 'Luxemburg', 'LU'],
                    'Malta': ['Malta', 'MT'],
                    'Moldova': ['Moldova', 'MD'],
                    'Monaco': ['Monaco', 'MC'],
                    'Montenegro': ['Montenegro', 'Crna', 'Gora',  'ME'],
                    'Netherlands': ['Netherlands', 'Holland', 'Nederland', 'NL'],
                    'North Macedonia': ['Macedonia', 'MK'],
                    'Norway': ['Norway', 'Norge', 'NO'],
                    'Poland': ['Poland', 'Polska', 'PO'],
                    'Portugal': ['Portugal', 'Portuguesa', 'PT'],
                    'Romania': ['Romania', 'RO'],
                    'Russia': ['Russia', 'Rossiya', 'RU'],
                    'San Marino': ['Marino', 'SM'],
                    'Serbia': ['Serbia', 'Srbija', 'RS'],
                    'Slovakia': ['Slovakia', 'Slovak', 'Slovenská', 'SK'],
                    'Slovenia': ['Slovenia', 'SL'],
                    'Spain': ['Spain', 'España', 'ES'],
                    'Sweden': ['Sweden', 'Sverige', 'SE'],
                    'Switzerland': ['Switzerland', 'Swiss', 'Schweizerische', 'CH'],
                    'Turkey': ['Turkey', 'Türkiye', 'TR'],
                    'Ukraine': ['Ukraine', 'Ukraïna', 'UA'],
                    'Vatican City': ['Vatican', 'VA']}

    country_list = []
    for idx, location in enumerate(dataset['location']):
        country_found = False
        if idx % 100000 == 0:
            print(idx, '/', dataset.shape[0])

        for country in country_dict:
            if pd.isna(location):
                break

            for word in re.sub(r'[^\w\s]', '', location).split(' '):
                for pattern in country_dict[country]:
                    if pattern.lower() == word.lower():
                        country_list.append(country)
                        country_found = True
                        break
                if country_found:
                    break
            if country_found:
                break

        if not country_found:
            country_list.append('')

    dataset['country'] = country_list

    return dataset


def main():


    df_syr = pd.read_csv("New/combine_syr_extra.csv")
    df_ukr = pd.read_csv("New/_combine_ukr_extra.csv")

    df_syr = find_country(df_syr)
    df_ukr = find_country(df_ukr)

    df_syr.to_csv("New/combine_syr_extra.csv", index=False)
    df_ukr.to_csv("New/_combine_ukr_extra.csv", index=False)


if __name__ == "__main__":
    main()