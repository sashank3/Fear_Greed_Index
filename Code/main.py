import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from WSJ_Scraper import scrape_wsj_business
from Data_Cleaning import clean_data, filter_article_dataset, data_saver
from Feature_Engineering import generate_subdomain_feature

# -----------------------------------------------------------------------------------------------------------------------

# Scrape the webpage and get new articles data
articles_data = scrape_wsj_business()
clean_df = clean_data(articles_data)
filtered_df = filter_article_dataset(clean_df)
feature_df = generate_subdomain_feature(filtered_df)
sentiment_df = ???
data_saver(sentiment_df)
ema_streamlit_stuff = ???


# -----------------------------------------------------------------------------------------------------------------------






