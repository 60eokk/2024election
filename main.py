import requests
from collections import Counter
import re  # Add this line to import the re module
import json
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


def fetch_articles(api_key, keyword, page_size=10):
    """Fetch articles from The Guardian API for a given keyword."""
    base_url = "https://content.guardianapis.com/search"
    params = {
        'api-key': api_key,
        'q': keyword,
        'page-size': page_size,
        'show-fields': 'body'  # Request the body field to get article text
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return [(article['webTitle'], article['fields']['body']) for article in data['response']['results']]

def count_words(text):
    """Count words in a text, excluding common stop words."""
    stop_words = set(["the", "to", "of", "a", "that", "and", "in", "is", "for", "on", "with"])
    words = re.findall(r'\b\w+\b', text.lower())
    filtered_words = [word for word in words if word not in stop_words and len(word) > 1]
    word_counts = Counter(filtered_words)
    return word_counts

def aggregate_rankings(articles):
    """Aggregate word rankings from a list of articles."""
    word_ranking_sums = Counter()
    for title, body in articles:
        word_counts = count_words(body)
        word_ranking_sums.update(word_counts)
    return word_ranking_sums.most_common(10)

def plot_keyword_rankings(rankings, keyword):
    """Plot a bar graph of the top word rankings for a given keyword."""
    words, scores = zip(*rankings)
    plt.figure(figsize=(10, 6))
    plt.bar(words, scores, color='skyblue')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title(f'Top Word Rankings for {keyword}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    api_key = '2ce72283-ccba-4b1a-92da-2f702366b61c'
    keywords = ['Trump', 'Biden']
    for keyword in keywords:
        articles = fetch_articles(api_key, keyword, page_size=10)
        rankings = aggregate_rankings(articles)
        plot_keyword_rankings(rankings, keyword)

if __name__ == "__main__":
    main()
