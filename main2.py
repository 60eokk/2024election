# Approach to implement HuggingFace's NLP Models
# In order to so: Will do by starting over, and taking functions from main.py

import requests
# from theguardian import theguardian_content
from bs4 import BeautifulSoup
# pipeline for high level API in library (for pretrained models, NLP tasks)
# AutoTokenizaer for loading correct tokenizer for for given pretrained model (raw text to format that model can understand)
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import sqlite3
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report





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

def create_table():
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS articles
                 (id TEXT PRIMARY KEY, title TEXT, date TEXT, content TEXT)''')
    conn.commit()
    conn.close()


# SQL commands
def to_sqlite(articles):
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    
    for article in articles:
        article_id = article['id']
        title = article['webTitle']
        date = article['webPublicationDate']
        if 'fields':
            content = article['fields']['body']
        else:
            content = ''

        c.execute("INSERT OR IGNORE INTO articles (id, title, date, content) VALUES (?,?,?,?)", (article_id, title, date, content))

    conn.commit()
    conn.close()


def main():
    apikey = '2ce72283-ccba-4b1a-92da-2f702366b61c'

    # Load pre-trained models
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

    create_table()

    # test case
    keyword, from_date, to_date, page_size = "Trump", '2020-01-01', '2020-12-31', '2'
    articles = fetch_articles(apikey, keyword, from_date, to_date, page_size)
    # print(example_articles)
    # clean_data(fetch_articles)
    
    # Save db so that SQL can be used
    to_sqlite(articles)
    
    conn = sqlite3.connect('articles.db')
    df = pd.read_sql_query("SELECT * FROM articles", conn)
    conn.close()

    df.to_csv('articles.csv', index=False)

    #SQL results
    print("SQL Results:")
    print(df)

        # Clean the content data
    df['clean_content'] = df['content'].apply(clean_data)

    # Get sentiment labels for training
    df['sentiment'], df['sentiment_score'] = zip(*df['clean_content'].apply(lambda x: sentiment_analysis(x, sentiment_pipeline)))

    # Convert sentiment labels to binary labels (positive/negative)
    df['sentiment_label'] = df['sentiment'].apply(lambda x: 1 if x == 'POSITIVE' else 0)

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(df['clean_content'], df['sentiment_label'], test_size=0.2, random_state=42)

    # Vectorize the text data
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Train a logistic regression model
    model = LogisticRegression()
    model.fit(X_train_vec, y_train)

    # Make predictions
    y_pred = model.predict(X_test_vec)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f"Model Accuracy: {accuracy}")
    print("Classification Report:")
    print(report)


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