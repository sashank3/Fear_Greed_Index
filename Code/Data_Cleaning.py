import pandas as pd

# Determines which articles are duplicates among the newly scraped data itself, not with articles.csv.
def clean_data(df):
    # Remove repeated articles
    df = df.drop_duplicates(subset='Title')
    print('Success! - Duplicate Removal')
    return df


# Determines which articles are already present on the articles.csv file, and returns only newly scraped data.
def filter_article_dataset(df):
    try:
        existing_df = pd.read_csv('articles_features.csv')
        existing_titles = set(existing_df['Title'])
        df_unique = df[~df['Title'].isin(existing_titles)]
        print('Success! - Data Filtering')
        return df_unique

    except FileNotFoundError:
        print('Success! - Data Filtering')
        return df


# Saves the newly scraped data to articles.csv
def data_saver(df, filename='articles_features'):
    try:
        existing_df = pd.read_csv(filename + '.csv')
    except FileNotFoundError:
        existing_df = pd.DataFrame(columns=['Title', 'Time', 'Link', 'Subdomain', 'Sentiment'])

    # Append the new data to the existing DataFrame
    merged_df = pd.concat([existing_df, df], ignore_index=True)

    # Save the merged DataFrame to the CSV file
    merged_df.to_csv('Data/' + filename + '.csv', index=False, encoding='utf-8-sig')
    print('Success! - Data Saved')