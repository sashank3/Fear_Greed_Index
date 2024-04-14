import pandas as pd


# Regex to find the Subdomain of an article based on its URL.
def extract_subdomain(link):
    parts = link.split('/')
    subdomain = parts[3].capitalize()
    if subdomain in ['Business', 'Tech']:
        subdomain = 'Business'
    elif subdomain == 'Economy':
        subdomain = 'Economy'
    elif subdomain in ['Finance', 'Personal-finance']:
        subdomain = 'Finance'
    elif subdomain == 'Health':
        subdomain = 'Health'
    elif subdomain in ['Politics', 'Us-news', 'World']:
        subdomain = 'Politics'
    elif subdomain == 'Real-estate':
        subdomain = 'Real-Estate'
    else:
        subdomain = 'Articles'
    return subdomain


def generate_subdomain_feature(df):
    # Add new column 'subdomain' to the DataFrame
    df['Subdomain'] = df['Link'].apply(extract_subdomain)
    print('Success! - Feature Engineering')
    return df


# Define a function to calculate EMA for each subgroup (subdomain) of the DataFrame
def generate_ema():
    df = pd.read_csv('Data/articles_features.csv')
    # Convert 'Time' column to datetime format
    df['Time'] = pd.to_datetime(df['Time'])

    # Define a function to calculate labels for each EMA range
    def calculate_label(ema):
        if ema <= 20:
            return 'Extreme Fear'
        elif ema <= 40:
            return 'Fear'
        elif ema <= 60:
            return 'Neutral'
        elif ema <= 80:
            return 'Greed'
        else:
            return 'Extreme Greed'

    # Initialize an empty list to store the DataFrames for each subdomain
    ema_data_list = []

    # Define a function to calculate EMA for each subdomain
    def calculate_subdomain_ema(subdomain_data):
        # Calculate the EMAs for different spans
        ema_7_days = subdomain_data['Sentiment'].ewm(span=7, adjust=False).mean().iloc[-1]
        ema_21_days = subdomain_data['Sentiment'].ewm(span=21, adjust=False).mean().iloc[-1]
        ema_60_days = subdomain_data['Sentiment'].ewm(span=60, adjust=False).mean().iloc[-1]
        ema_7_days = round((ema_7_days) * 25, 0)
        ema_21_days = round((ema_21_days) * 25, 0)
        ema_60_days = round((ema_60_days) * 25, 0)

        # Calculate labels for each EMA range
        label_7_days = calculate_label(ema_7_days)
        label_21_days = calculate_label(ema_21_days)
        label_60_days = calculate_label(ema_60_days)

        # Create a DataFrame for the current subdomain's EMAs
        subdomain_ema_data = pd.DataFrame({'Subdomain': subdomain_data['Subdomain'].iloc[0],
                                           'EMA_7_days': ema_7_days,
                                           'EMA_21_days': ema_21_days,
                                           'EMA_60_days': ema_60_days,
                                           'Label_7_days': label_7_days,
                                           'Label_21_days': label_21_days,
                                           'Label_60_days': label_60_days}, index=[0])

        return subdomain_ema_data

    # Group data by subdomain and apply the function to calculate EMA for each group
    ema_data = df.groupby('Subdomain').apply(calculate_subdomain_ema).reset_index(drop=True)

    return ema_data

