# NEWSAPI usage below

from newsapi import NewsApiClient
from collections import Counter
import re
import json
import requests
from bs4 import BeautifulSoup

def count_words(text):
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)
    return word_counts.most_common()

def fetch_article_text(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            article_text = ' '.join([p.get_text() for p in paragraphs])
            return article_text
        else:
            print(f"Failed to fetch the article: HTTP {response.status_code}")
            return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

def main():
    api_key = '286057e277b5469db123953b0e0d0214'
    api = NewsApiClient(api_key=api_key)
    keyword = 'Trump'

    articles = api.get_everything(q=keyword)
    all_rankings = []

    for article in articles['articles']:
        url = article['url']
        title = article['title']
        print(f"Processing article: {title}")
        
        article_text = fetch_article_text(url)
        ranked_words = count_words(article_text)

        all_rankings.append({
            'title': title,
            'url': url,
            'word_rankings': ranked_words[:10]
        })

    with open(f'word_rankings_for_{keyword}.json', 'w') as f:
        json.dump(all_rankings, f, indent=4)

    print(f"Word rankings for all articles related to '{keyword}' have been saved.")

if __name__ == "__main__":
    main()
