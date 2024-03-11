import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import sqlite3


# Helper functions
def convert_relative_time(relative_time):
    if 'hour' in relative_time:
        hours_ago = int(relative_time.split()[0])
        return (datetime.now() - timedelta(hours=hours_ago)).strftime('%Y-%m-%d %H:%M')

    elif 'day' in relative_time:
        days_ago = int(relative_time.split()[0])
        return (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M')
    # Add more conditions for other units if needed
    else:
        return None  # Handle unsupported formats


# Function to scrape the webpage
def scrape_wsj_business():
    # URL of the webpage to scrape
    urls = ['https://www.wsj.com/business',
            'https://www.wsj.com/finance',
            'https://www.wsj.com/real-estate']#,
            # 'https://www.wsj.com/business/autos',
            # 'https://www.wsj.com/business/earnings',
            # 'https://www.wsj.com/business/energy-oil',
            # 'https://www.wsj.com/business/small-business-marketing',
            # 'https://www.wsj.com/business/telecom',
            # 'https://www.wsj.com/business/retail',
            # 'https://www.wsj.com/business/logistics',
            # 'https://www.wsj.com/business/hospitality',
            # 'https://www.wsj.com/finance/banking',
            # 'https://www.wsj.com/finance/commodities-futures',
            # 'https://www.wsj.com/finance/currencies',
            # 'https://www.wsj.com/finance/stocks',
            # 'https://www.wsj.com/finance/regulation',
            # 'https://www.wsj.com/finance/investing']

    # Define custom headers to mimic a real web browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.36'
    }

    # Initialize lists to store the titles and text content of the articles
    articles_data = []

    for url in urls:

        # Sleep for a few seconds to mimic human behavior
        time.sleep(2)

        # Send a GET request to the URL with custom headers
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the webpage
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all the articles on the webpage
            articles = soup.find_all('h3', class_='css-fsvegl')

            # Loop through each article and extract the title and text content
            for article in articles:
                # Find the next <p> tag after the <h3> tag
                p_tag = article.find_next_sibling('p')
                if p_tag:
                    title = article.text.strip()
                    content = p_tag.text.strip()
                    time_tag = p_tag.find_next('p', class_=lambda c: c and 'TimeTag' in c)
                    if time_tag:
                        time_formatted = time_tag.text.strip()
                    articles_data.append((title, content, convert_relative_time(time_formatted)))


        else:
            # If the request was not successful, print an error message
            print('Error: Failed to retrieve webpage.')

    # Return the titles and text content as a tuple of lists
    return articles_data


def save_to_database(articles_data):
    # Connect to the SQLite database
    conn = sqlite3.connect('articles.db')
    cursor = conn.cursor()

    # Create the articles table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS articles
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT,
                      content TEXT,
                      time TEXT)''')

    # Insert the articles data into the database
    cursor.executemany('''INSERT INTO articles (title, content, time)
                          VALUES (?, ?, ?)''', articles_data)

    # Commit changes and close connection
    conn.commit()
    conn.close()


# Scrape the webpage and get articles data
articles_data = scrape_wsj_business()
print(articles_data)

# Save the articles data to SQLite database
save_to_database(articles_data)

