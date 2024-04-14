import torch
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer

if torch.cuda.is_available():
    device = "cuda"

print(device)

model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", torch_dtype="auto", trust_remote_code=True).to(device)
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)

#obtain data
df = pd.read_csv('articles_test.csv')

prompt = ("Instruct: As a Financial News Article Sentiment Classification expert, analyze the sentiment of the following financial news article "
          "and classify its sentiment as a single number, 0 being 'Negative', 1 being 'Neutral', and 2 being 'Positive'. Provide only a single "
          "number as output, without additional text. Below is an example to illustrate the sentiment classification:\n Example 1: 'Finnish electronics "
          "manufacturing services EMS company Elcoteq SE posted a net loss of 66.4 mln euro $ 91.2 mln for the first half of 2007 , compared to a net "
          "profit of 7.1 mln euro $ 9.8 mln for the same period of 2006 .' - Output:0 \n Example 2: 'In January-September 2009 , the Group 's net "
          "interest income increased to EUR 112.4 mn from EUR 74.3 mn in January-September 2008 .' - Output:2 \n Sentiment Classification news article: ")


predictions = []

for sentence in data:
    inputs = tokenizer([prompt + "'" + sentence + "' \n Output:"], return_tensors="pt", return_attention_mask=False).to(device)
    outputs = model.generate(**inputs, max_new_tokens=20, pad_token_id=model.config.eos_token_id)
    text = tokenizer.batch_decode(outputs)
    predictions.append(int(text[-1][-15]))

df['sentiment'] = predictions???


# Save the DataFrame to same CSV file
df.to_csv('articles.csv', index=False)??? Does it replace?


print("LLM Sentiment added successfully.")

