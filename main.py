# another version of NEWSAPI


from newsapi import NewsApiClient
from collections import Counter
import re
import json
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# Define a list of common English words to exclude
stop_words = set(["the", "to", "of", "a", "that", "and", "in", "is", "for", "on", "with"])

def count_words(text):
    words = re.findall(r'\b\w+\b', text.lower())
    filtered_words = [word for word in words if word not in stop_words]
    word_counts = Counter(filtered_words)
    return word_counts.most_common()

def fetch_article_text(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            article_text = ' '.join(p.get_text() for p in paragraphs)
            return article_text
        else:
            print(f"Failed to fetch the article: HTTP {response.status_code}")
            return ""  # Return an empty string for articles that can't be fetched
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""  # Return an empty string for any other errors


def read_top_aggregated_rankings(filename, top_n=10):
    rankings = {}
    with open(filename, 'r') as f:
        for line in f.readlines()[:top_n]:
            parts = line.strip().split(': ')
            word, rank = parts[0], int(parts[1])
            rankings[word] = rank
    return rankings

def plot_keyword_rankings(rankings, keyword):
    words = list(rankings.keys())
    scores = list(rankings.values())
    plt.figure(figsize=(10, 6))
    plt.bar(words, scores, color='skyblue')
    plt.xlabel('Words')
    plt.ylabel('Total Aggregated Ranking')
    plt.title(f'Top Word Rankings for {keyword}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def process_keyword(api_key, keyword):
    api = NewsApiClient(api_key=api_key)
    articles = api.get_everything(q=keyword, language='en', sort_by='relevancy')
    word_ranking_sums = Counter()

    for article in articles['articles']:
        article_text = fetch_article_text(article['url'])
        ranked_words = count_words(article_text)
        for word, _ in ranked_words:
            word_ranking_sums[word] += 1

    sorted_aggregate_rankings = word_ranking_sums.most_common(10)
    aggregated_filename = f'aggregated_rankings_for_{keyword}.txt'
    with open(aggregated_filename, 'w') as f:
        for word, total_ranking in sorted_aggregate_rankings:
            f.write(f"{word}: {total_ranking}\n")

    print(f"Aggregated word rankings for {keyword} have been saved to '{aggregated_filename}'.")

def main():
    api_key = '286057e277b5469db123953b0e0d0214'
    keywords = ['Trump', 'Biden']

    for keyword in keywords:
        process_keyword(api_key, keyword)
        aggregated_filename = f'aggregated_rankings_for_{keyword}.txt'
        top_rankings = read_top_aggregated_rankings(aggregated_filename, top_n=10)
        plot_keyword_rankings(top_rankings, keyword)

if __name__ == "__main__":
    main()
