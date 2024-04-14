import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta


# Helper functions
def convert_relative_time(relative_time):

    if 'hour' in relative_time:
        hours_ago = int(relative_time.split()[0])
        return (datetime.now() - timedelta(hours=hours_ago)).strftime('%Y-%m-%d %H:%M')

    elif '2024' in relative_time:
        parsed_date = datetime.strptime(relative_time, '%B %d, %Y')
        return parsed_date.strftime('%Y-%m-%d %H:%M')
    # Add more conditions for other units if needed
    else:
        return datetime.now().strftime('%Y-%m-%d %H:%M')


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
        'Pragma': 'no-cache',
        'Origin': 'https://www.wsj.com',
        'Accept-Language': 'en-US,en;q=0.9',
        'Sec-WebSocket-Key': 'A/siKlupV2NvtfZwYZ3f3Q==',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        'Upgrade': 'websocket',
        'Cache-Control': 'no-cache',
        'Connection': 'Upgrade',
        'Sec-WebSocket-Version': '13',
        'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
    }

    params = {
        'transport': 'webSockets',
        'clientProtocol': '2.1',
        'connectionToken': '776a6d01-9b67-4c26-a392-8381c94e4700:',
        'connectionData': '[{"name":"mainhub"}]',
        'tid': '0',
    }

    # Initialize lists to store the titles and text content of the articles
    articles_data = []

    for url in urls:

        # Sleep for a few seconds to mimic human behavior
        time.sleep(2)

        # Send a GET request to the URL with custom headers
        response = requests.get(url, params=params, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the webpage
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all the articles on the webpage
            articles = soup.find_all('h3', class_='css-fsvegl')

            # Loop through each article and extract the title and text content
            for article in articles:


                # Find the first <a> tag within the <h3> tag

                # if a_tag:
                #     # Extract the href attribute
                #     href = a_tag['href']
                #
                #     # Send a GET request to the linked page
                #     linked_response = requests.get(href, params=params, headers=headers)
                #     print(linked_response)
                #     if linked_response.status_code == 200:
                #         # Parse the HTML content of the linked page
                #         linked_soup = BeautifulSoup(linked_response.text, 'html.parser')
                #
                #         # Find all the paragraphs on the linked page
                #         paragraphs = linked_soup.find_all('p')
                #
                #         # Extract the text content of each paragraph and append to content
                #         content = ' '.join([p.text.strip() for p in paragraphs])
                #     else:
                #         # If the request to the linked page was not successful, skip this article
                #         print(f'Error: Failed to retrieve content from {href}')
                #         break

                    # Extract the title from the anchor tag
                a_tag = article.find('a')
                href = a_tag['href']
                title = article.text.strip()

                # Extract the relative time
                time_tag = article.find_next('p', class_=lambda c: c and 'TimeTag' in c)
                time_formatted = None
                if time_tag:
                    time_formatted = time_tag.text.strip()

                # Append the extracted information to articles_data
                articles_data.append((title, convert_relative_time(time_formatted), href))



        else:
            # If the request was not successful, print an error message
            print('Error: Failed to retrieve webpage.')

    # Return the titles and text content as a tuple of lists
    return articles_data


