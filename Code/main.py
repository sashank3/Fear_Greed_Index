from WSJ_Scraper import scrape_wsj_business
from Data_Cleaning import clean_data, filter_article_dataset, data_saver
from Feature_Engineering import generate_subdomain_feature, generate_ema
from LLM import predict_sentiment

# -----------------------------------------------------------------------------------------------------------------------

# Scrape the webpage and get new articles data
articles_data = scrape_wsj_business()
clean_df = clean_data(articles_data)
filtered_df = filter_article_dataset(clean_df)
feature_df = generate_subdomain_feature(filtered_df)
sentiment_df = predict_sentiment(feature_df)
data_saver(sentiment_df)
categorical_ema = generate_ema()

# -----------------------------------------------------------------------------------------------------------------------






