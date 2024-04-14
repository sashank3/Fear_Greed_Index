import pandas as pd
import random
from datetime import datetime, timedelta

# Read existing data from the CSV file
df = pd.read_csv('articles_test.csv')

# Duplicate each row twice and append them to the DataFrame
df = pd.concat([df] * 4, ignore_index=True)

# Add new columns 'sentiment' and 'subdomain' to the DataFrame
df['sentiment'] = [random.randint(1, 5) for _ in range(len(df))]
df['subdomain'] = [random.choice(['Banking', 'Healthcare']) for _ in range(len(df))]

# Calculate the number of rows in the DataFrame
num_rows = len(df)

# Generate a series of dates starting from the current day and going back
# to the current day minus the number of rows
start_date = datetime.now()
dates = [start_date - timedelta(days=i) for i in range(num_rows)]

# Update the 'time' column for each row with the generated dates
df['time'] = [date.strftime('%Y-%m-%d %H:%M:%S') for date in dates]

# Save the DataFrame to a new CSV file
df.to_csv('articles_modified.csv', index=False)

# Print the modified DataFrame
print(df)

print("Columns 'sentiment' and 'subdomain' added successfully.")
