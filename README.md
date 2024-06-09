# The Fear & Greed Index: Small Language Models (SLMs)
 <br/>
Let's begin by asking a simple question: Are individual investors informed?
<br/><br/>

![image](https://github.com/sashank3/Fear_Greed_Index/assets/41186713/3b2e8169-fa98-4e2c-af41-032ee16f6304)

<br/>

Well, the answer is NO. How could a single individual compete against Teams of Ivy League Quants with Billions in funding? This is where my tool comes into the picture. 

It aims to provide high-quality market sentiment data using SLMs through an easy-to-interpret Fear & Greed Index, enabling individual investors to make more informed decisions.

<br/>

## System Architecture

![image](https://github.com/sashank3/Fear_Greed_Index/assets/41186713/3a7c6858-4c7d-437d-b26f-540b047a8418)

<br/>

**Web Scraper** - Obtains the latest news articles from the Wall Street Journal website using Beautiful Soup and Data Scraping.<br/>
**Data Cleaning** - Parses and formats the scraped data, while eliminating duplicate articles using Python and Regex.<br/>
**Feature Engineering** - Categorizes cleaned data into financial subdomains like Real Estate, US Markets, etc. <br/>
**Phi-2 SLM** - Performs sentiment analysis on news articles using a prompt engineered Phi-2 Small Language Model.<br/>

<br/>

## Fear & Greed Investor Dashboard

![image](https://github.com/sashank3/Fear_Greed_Index/assets/41186713/d226a6f0-a4fa-4ed9-bff0-35efbceee0e8)



