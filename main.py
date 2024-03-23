# another version of NEWSAPI


from newsapi import NewsApiClient
from collections import Counter
import re
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime  

def count_words(text):
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)
    return word_counts.most_common()

def fetch_article_text(url):
    headers = {'User-Agent': 'Mozilla/5.0'}  # Adding a User-Agent header
    try:
        response = requests.get(url, headers=headers, timeout=10)  # Added timeout
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            article_text = ' '.join([p.get_text() for p in paragraphs])
            return article_text
        else:
            print(f"Failed to fetch the article: HTTP {response.status_code}")
            return ""
    except Exception as e:
        print(f"An error occurred while fetching the article: {e}")
        return ""

def main():
    api_key = '286057e277b5469db123953b0e0d0214'
    api = NewsApiClient(api_key=api_key)
    keyword = 'Trump'

    # Set time range
    from_date = '2020-01-01'
    to_date = '2020-12-31'

    # Added language parameter to filter for English articles
    articles = api.get_everything(q=keyword, 
                                  from_param=from_date, 
                                  to=to_date,
                                  language='en',  # Assuming you want articles in English
                                  sort_by='relevancy')
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
            'word_rankings': ranked_words[:10]  # Consider limiting this if the output is too verbose
        })

    filename = f'word_rankings_for_{keyword}.json'
    with open(filename, 'w') as f:
        json.dump(all_rankings, f, indent=4)

    print(f"Word rankings for all articles related to '{keyword}' have been saved to {filename}.")

if __name__ == "__main__":
    main()