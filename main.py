import requests
from collections import Counter
import re
from bs4 import BeautifulSoup
# import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import nltk
import plotly.express as px
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer


def fetch_articles(api_key, keyword, page_size):
    """Fetch articles from The Guardian API for a given keyword."""
    print(f"Fetching articles for '{keyword}'...")
    base_url = "https://content.guardianapis.com/search"
    params = {
        'api-key': api_key,
        'q': keyword,
        'page-size': page_size,
        'show-fields': 'body',  # Request the body field to get article text
        'from-date' : '2012-01-01',
        'to-date' : '2012-12-31'
    }
    constructed_url = requests.Request('GET', base_url, params=params).prepare().url
    print(f"Constructed URL for '{keyword}': {constructed_url}")  # Print the constructed URL for manual checking
    
    try:
        response = requests.get(constructed_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = data['response']['results']
        if not articles:
            print(f"No articles found for '{keyword}'.")
            return []
        print(f"Fetched {len(articles)} articles for '{keyword}'.")
        return [(article['webTitle'], article['fields']['body']) for article in articles if 'body' in article['fields']]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while fetching articles for '{keyword}': {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Request error while fetching articles for '{keyword}': {err}")
    return []


nltk.download('stopwords')

def count_words(text):
    """Count words in a text, excluding common stop words."""
    stop_words = set(stopwords.words('english'))
    # Extend the stop words list with custom words specific to your dataset
    custom_stop_words = ["https", "com", "theguardian", "href", "www", "class", "block", "time", "div", "id", "h2", "figure", "elements"]
    stop_words.update(custom_stop_words)
    
    words = re.findall(r'\b\w+\b', text.lower())
    filtered_words = [word for word in words if word not in stop_words and len(word) > 1]
    return Counter(filtered_words)

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def aggregate_rankings(articles, keyword):  # Added keyword as a parameter
    """Aggregate word rankings from a list of articles."""
    print(f"Aggregating rankings for {len(articles)} articles...")
    word_ranking_sums = Counter()
    sentiments = []
    for title, body in articles:
        word_counts = count_words(body)
        word_ranking_sums.update(word_counts)
        sentiment = analyze_sentiment(body)
        sentiments.append(sentiment)
    average_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
    print(f"Average sentiment for '{keyword}': {average_sentiment}")  # keyword is now defined in this scope
    return word_ranking_sums.most_common(20), average_sentiment


def plot_keyword_rankings_interactive(rankings, keyword):
    if rankings:
        words, scores = zip(*rankings)
        fig = px.bar(x=words, y=scores, title=f'Top Word Rankings for {keyword}', labels={'x':'Words', 'y':'Frequency'})
        fig.show()
    else:
        print(f"No data to plot for '{keyword}'.")

def main():
    api_key = '2ce72283-ccba-4b1a-92da-2f702366b61c'  # Replace with your actual API key
    keywords = ['Obama', 'Romney']
    for keyword in keywords:
        articles = fetch_articles(api_key, keyword, page_size=50)
        if articles:
            rankings, average_sentiment = aggregate_rankings(articles, keyword)
            print(f"Plotting interactive rankings for {keyword}")
            plot_keyword_rankings_interactive(rankings, keyword)  # Use the interactive plotting function
            print(f"Average sentiment for {keyword}: {average_sentiment}")
        else:
            print(f"No articles fetched for '{keyword}', skipping plotting.")

if __name__ == "__main__":
    main()