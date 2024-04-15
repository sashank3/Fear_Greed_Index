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


def calculate_sliding_bucket_ema(sentiment_df):
    sentiment_df['Time'] = pd.to_datetime(sentiment_df['Time'])
    sentiment_df['Time'] = sentiment_df['Time'].dt.date
    new_df = sentiment_df.groupby(['Subdomain', 'Time'])['Sentiment'].mean().reset_index()
    new_df['Time'] = pd.to_datetime(new_df['Time'])
    new_df['Time'] = new_df['Time'].dt.date

    date_range_df = pd.DataFrame()
    for subdomain, group in new_df.groupby('Subdomain'):
        min_date = group['Time'].min()
        max_date = group['Time'].max()
        all_dates = pd.date_range(start=min_date, end=max_date)
        subdomain_dates_df = pd.DataFrame({'Time': all_dates, 'Subdomain': subdomain})
        date_range_df = pd.concat([date_range_df, subdomain_dates_df]).reset_index(drop=True)

    # Convert the 'Time' column in date_range_df to datetime
    date_range_df['Time'] = pd.to_datetime(date_range_df['Time'])
    date_range_df['Time'] = date_range_df['Time'].dt.date

    # Merge the calculated sentiment data with the DataFrame containing all possible dates
    merged_df = pd.merge(date_range_df, new_df, on=['Subdomain', 'Time'], how='left')

    merged_df['Sentiment'].fillna(2, inplace=True)
    merged_df['Sentiment'] = (merged_df['Sentiment'] * 25).round(0).astype(int)

    bucket_sizes = [4, 12, 30]

    ema_data = pd.DataFrame()
    for subdomain, group in merged_df.groupby('Subdomain'):
        subdomain_ema = pd.DataFrame({'Time': group['Time'], 'Subdomain': subdomain})
        for bucket_size in bucket_sizes:
            ema_column_name = f'EMA_{bucket_size}_days'
            ema_values = group['Sentiment'].ewm(span=bucket_size, adjust=False).mean()
            subdomain_ema[ema_column_name] = (ema_values).astype(int)
        ema_data = pd.concat([ema_data, subdomain_ema])

    # Reset index
    ema_data.reset_index(drop=True, inplace=True)

    return ema_data


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

    # Define a function to calculate EMA for each subdomain
    def calculate_subdomain_ema(subdomain_data):
        # Calculate the EMAs for different spans
        ema_4_days = subdomain_data['Sentiment'].ewm(span=4, adjust=False).mean().iloc[-1]
        ema_12_days = subdomain_data['Sentiment'].ewm(span=12, adjust=False).mean().iloc[-1]
        ema_30_days = subdomain_data['Sentiment'].ewm(span=30, adjust=False).mean().iloc[-1]
        ema_4_days = round(ema_4_days * 25, 0)
        ema_12_days = round(ema_12_days * 25, 0)
        ema_30_days = round(ema_30_days * 25, 0)

        # Calculate labels for each EMA range
        label_4_days = calculate_label(ema_4_days)
        label_12_days = calculate_label(ema_12_days)
        label_30_days = calculate_label(ema_30_days)

        # Create a DataFrame for the current subdomain's EMAs
        subdomain_ema_data = pd.DataFrame({'Subdomain': subdomain_data['Subdomain'].iloc[0],
                                           'EMA_4_days': ema_4_days,
                                           'EMA_12_days': ema_12_days,
                                           'EMA_30_days': ema_30_days,
                                           'Label_4_days': label_4_days,
                                           'Label_12_days': label_12_days,
                                           'Label_30_days': label_30_days}, index=[0])

        return subdomain_ema_data

    # Group data by subdomain and apply the function to calculate EMA for each group
    ema_data = df.groupby('Subdomain').apply(calculate_subdomain_ema).reset_index(drop=True)
    sliding_bucket_ema = calculate_sliding_bucket_ema(df)
    return ema_data, sliding_bucket_ema
