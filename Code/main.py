from WSJ_Scraper import scrape_wsj_business
from Data_Cleaning import clean_data, filter_article_dataset, data_saver
from Feature_Engineering import generate_subdomain_feature, generate_ema
from LLM import predict_sentiment
from Graphs import line_graph, gauge_chart

# -----------------------------------------------------------------------------------------------------------------------

# Scrape the webpage and get new articles data
articles_data = scrape_wsj_business()
clean_df = clean_data(articles_data)
filtered_df = filter_article_dataset(clean_df)

# Only run sentiment analysis if new articles are detected.
if filtered_df.shape[0] != 0:
    feature_df = generate_subdomain_feature(filtered_df)
    sentiment_df = predict_sentiment(feature_df)
    data_saver(sentiment_df)

# Fear and Greed Index
categorical_ema, sliding_ema = generate_ema()
gauge_chart(categorical_ema)
line_graph(sliding_ema)

# -----------------------------------------------------------------------------------------------------------------------
