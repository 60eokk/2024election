# NEWSAPI usage below

from newsapi import NewsApiClient
from collections import Counter
import re
import json

def count_words(text):
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)
    return word_counts.most_common()

def fetch_article_text(url):
    # Placeholder for your article fetching and text extraction logic
    # Replace this part with your actual implementation
    article_text = "Example fetched article text. Replace this with actual fetched content."
    return article_text

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
            'word_rankings': ranked_words[:10]  # Adjust the slice as needed
        })

    # Saving the rankings to a file
    with open(f'word_rankings_for_{keyword}.json', 'w') as f:
        json.dump(all_rankings, f, indent=4)

    print(f"Word rankings for all articles related to '{keyword}' have been saved to 'word_rankings_for_{keyword}.json'")

if __name__ == "__main__":
    main()
