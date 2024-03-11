import sqlite3
import random

# Connect to the SQLite database
conn = sqlite3.connect('articles.db')
cursor = conn.cursor()

# Add new columns 'sentiment' and 'subdomain' to the articles table
cursor.execute('''ALTER TABLE articles 
                  ADD COLUMN sentiment INTEGER''')

cursor.execute('''ALTER TABLE articles 
                  ADD COLUMN subdomain TEXT''')

# Define the list of subdomains
subdomains = ['Banking', 'Insurance', 'Real Estate', 'Cryptocurrency', 'Industrials',
              'Computers and Information Technology', 'Automotive', 'Retail', 'Energy',
              'Healthcare', 'Materials', 'Telecom']

# Update each row in the table with random values for 'sentiment' and 'subdomain'
cursor.execute('''SELECT id FROM articles''')
article_ids = cursor.fetchall()

for article_id in article_ids:
    sentiment = random.randint(1, 5)  # Random integer between 1 and 5
    subdomain = random.choice(subdomains)  # Randomly choose a subdomain from the list
    cursor.execute('''UPDATE articles 
                      SET sentiment = ?, subdomain = ?
                      WHERE id = ?''', (sentiment, subdomain, article_id[0]))

cursor.execute('''SELECT * FROM articles''')
rows = cursor.fetchall()

# Print the column names
column_names = [description[0] for description in cursor.description]
print(column_names)

# Print each row of data
for row in rows:
    print(row)

# Commit changes and close connection
conn.commit()
conn.close()

print("Columns 'sentiment' and 'subdomain' added successfully.")
