import pandas as pd
from datetime import datetime

# Load the data from the CSV file
df = pd.read_csv('articles_modified.csv')

# Convert the 'Time' column to datetime format
df['Time'] = pd.to_datetime(df['Time'])

# Separate data based on the last element of the tuple (subdomain)
subdomains = df['subdomain'].unique()

# Initialize an empty list to store the DataFrames for each subdomain
ema_data_list = []

# Define a function to calculate labels for each EMA range
def calculate_label(ema):
    if ema <= 20:
        return 'Extreme Fear'
    elif ema <= 45:
        return 'Fear'
    elif ema <= 55:
        return 'Neutral'
    elif ema <= 79:
        return 'Greed'
    else:
        return 'Extreme Greed'

for subdomain in subdomains:
    # Filter data for the current subdomain
    subdomain_data = df[df['subdomain'] == subdomain]

    # Calculate the EMAs for different spans
    ema_7_days = subdomain_data['sentiment'].ewm(span=7, adjust=False).mean().iloc[-1]
    ema_21_days = subdomain_data['sentiment'].ewm(span=21, adjust=False).mean().iloc[-1]
    ema_60_days = subdomain_data['sentiment'].ewm(span=60, adjust=False).mean().iloc[-1]
    ema_7_days = round((ema_7_days - 1) * 25, 0)
    ema_21_days = round((ema_21_days - 1) * 25, 0)
    ema_60_days = round((ema_60_days - 1) * 25, 0)

    # Calculate labels for each EMA range
    label_7_days = calculate_label(ema_7_days)
    label_21_days = calculate_label(ema_21_days)
    label_60_days = calculate_label(ema_60_days)

    # Create a DataFrame for the current subdomain's EMAs
    subdomain_ema_data = pd.DataFrame({'Subdomain': subdomain,
                                       'EMA_7_days': ema_7_days,
                                       'EMA_21_days': ema_21_days,
                                       'EMA_60_days': ema_60_days,
                                       'Label_7_days': label_7_days,
                                       'Label_21_days': label_21_days,
                                       'Label_60_days': label_60_days}, index=[0])

    # Append the DataFrame to the ema_data_list
    ema_data_list.append(subdomain_ema_data)

# Concatenate all DataFrames in the ema_data_list
ema_data = pd.concat(ema_data_list, ignore_index=True)

# Save the ema_data DataFrame to a CSV file
ema_data.to_csv('ema_results.csv', index=False)

# Display the ema_data DataFrame
print(ema_data)
