from transformers import AutoModelForCausalLM, AutoTokenizer


def load_model():
    model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", torch_dtype="auto", trust_remote_code=True).to(
        "cuda")
    tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)
    return model, tokenizer


def predict(model, tokenizer, sentence):
    prompt = (
        "Instruct: As a Financial News Article Sentiment Classification expert, analyze and classify the sentiment of "
        "the following news article as a single number ranging from 0 to 4, 0 being 'Very Negative' and 4 being "
        "'Very Positive'. Provide only a single number as output, without additional text. Below is a sentiment "
        "classification example:\n Example: 'Operating margin , however , slipped to 14.4 % from 15.1 % , "
        "dragged down by a poor performance in enterprise solutions .' - Output:0 \n Example: 'In January-September "
        "2009 , the Group 's net interest income increased to EUR 112.4 mn from EUR 74.3 mn in January-September 2008 "
        ".' - Output:4 \n Sentiment Classification news article: ")

    inputs = tokenizer([prompt + "'" + sentence + "' \n Output:"], return_tensors="pt", return_attention_mask=False).to(
        "cuda")
    outputs = model.generate(**inputs, max_new_tokens=1, pad_token_id=model.config.eos_token_id)
    text = tokenizer.batch_decode(outputs)
    return int(text[-1][-1])


def predict_sentiment(df):
    model, tokenizer = load_model()
    sentiments = []
    for sentence in df['Title']:
        sentiment = predict(model, tokenizer, sentence)
        sentiments.append(sentiment)

    df['Sentiment'] = sentiments
    print('Success! - LLM Sentiment Analysis')
    return df
