# Approach to implement HuggingFace's NLP Models
# In order to so: Will do by starting over, and taking functions from main.py

import requests
# from theguardian import theguardian_content
from bs4 import BeautifulSoup
# pipeline for high level API in library (for pretrained models, NLP tasks)
# AutoTokenizaer for loading correct tokenizer for for given pretrained model (raw text to format that model can understand)
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch






# 1. data collection (collect articles from past)
# fetch and load articles --> will later be stored in csv/excel/sql
def fetch_articles(apikey, keyword, from_date, to_date, page_size):
    print(f"Fetching articles for '{keyword}' from {from_date} to {to_date}!")
    url = "https://content.guardianapis.com/search"
    params = {
        'api-key': apikey,
        'q': keyword,
        'page-size': page_size, 
        'from-date': from_date,
        'to-date': to_date,
        'show-fields': 'body'
    }

    response = requests.get(url, params = params)

    if response.status_code == 200:
        # response.json converts API response from json to dictionary
        return response.json()['response']['results'] 
    else:
        return {response.status_code} # professional approach on errors

# 2. data processing (clean, process data)
# can this be done without clean_html. yes!
def clean_data(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')

    for script in soup(['script','style']):
        script.decompose() # getting rid of script, style components (ex. default, html)
    
    text = soup.get_text()

    words = text.split()
    text = ' '.join(words)

    return text



# 3. use nlp models to extract features (sentiment scores, etc)
# text processing: tokenization(implementation HuggingFace?), stopword, keyword, sentiment analysis
# Advanced NLP library: spaCy, TF-DIF, LDA, word embedding(Word2Vec, gloVe)
# Implementing Huggingface's Transformers library. 
# Would it be possible for fine-tuning in this project?
def sentiment_analysis(text, sentiment_pipeline):
    result = sentiment_pipeline(text[:512])[0] # 512 tokens due to model constraint
    return result['label'], result['score']

# Checking out a feature
def text_summarization(text, summarizer_pipeline):
    summary = summarizer_pipeline(text)[0]['summary_text']
    return summary


def main():
    apikey = '2ce72283-ccba-4b1a-92da-2f702366b61c'

    # Load pre-trained models
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

    # test case
    keyword, from_date, to_date, page_size = "Trump", '2020-01-01', '2020-12-31', '2'
    articles = fetch_articles(apikey, keyword, from_date, to_date, page_size)
    # print(example_articles)
    # clean_data(fetch_articles)

    for article in articles:
        print(f"Title: {article['webTitle']}")
        print(f"Date: {article['webPublicationDate']}")

        if 'fields':
            clean_body = clean_data(article['fields']['body'])
            print(f"Cleaned: \n{clean_body}")

        # Sentiment Analysis
            sentiment, confidence = sentiment_analysis(clean_body, sentiment_pipeline)
            print(f"\nSentiment: {sentiment}")
            print(f"Confidence: {confidence:.4f}")

            summary = text_summarization(clean_body, summarizer_pipeline)
            print(f"\nSummary: {summary}")

        else: 
            print("No content")

        print("\n----------\n")


if __name__ == "__main__": 
    main()





# 4. model training 
# 5. prediction