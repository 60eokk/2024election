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
    word_counts = Counter(words)
    return word_counts.most_common()

def fetch_article_text(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
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

def read_top_aggregated_rankings(filename, top_n=10):
    """Read aggregated rankings from a file and return the top N words and their total ranking sum."""
    rankings = {}
    with open(filename, 'r') as f:
        for line in f.readlines()[:top_n]:  # Only read the top N lines
            parts = line.strip().split(':')
            if len(parts) >= 2:
                word = parts[0].strip()
                # Find digits in the remainder of the line, assuming the ranking is the first integer found
                match = re.search(r'\d+', parts[1])
                if match:
                    total_ranking = int(match.group(0))
                    rankings[word] = total_ranking
    return rankings



def plot_keyword_rankings(rankings, keyword):
    """Plot a bar graph of the top word rankings for a given keyword."""
    words = list(rankings.keys())
    scores = list(rankings.values())
    plt.figure(figsize=(10, 8))
    plt.barh(words, scores, color='skyblue')
    plt.xlabel('Total Aggregated Ranking')
    plt.ylabel('Words')
    plt.title(f'Top Word Rankings for {keyword}')
    plt.gca().invert_yaxis()  # Invert y-axis to have the top ranking at the top
    plt.show()


def process_keyword(api_key, keyword):
    api = NewsApiClient(api_key=api_key)
    articles = api.get_everything(q=keyword, language='en')
    all_original_rankings = []
    all_filtered_rankings = []
    word_ranking_sums = {}

    for index, article in enumerate(articles['articles'], start=1):
        url = article['url']
        title = article['title']
        print(f"Processing article: {title}")
        
        article_text = fetch_article_text(url)
        ranked_words = count_words(article_text)
        
        all_original_rankings.append({
            'title': title,
            'url': url,
            'word_rankings': ranked_words[:10]
        })

        filtered_rankings = [(word, count) for word, count in ranked_words if word not in stop_words][:10]
        formatted_filtered_rankings = f"Article {index}: {title}\nURL: {url}\nTop words:\n" + \
                                      '\n'.join([f"{i+1}: {word} ({count} times)" for i, (word, count) in enumerate(filtered_rankings)]) + \
                                      "\n\n"
        all_filtered_rankings.append(formatted_filtered_rankings)
        
        for i, (word, _) in enumerate(filtered_rankings):
            word_ranking_sums[word] = word_ranking_sums.get(word, 0) + (i + 1)

    with open(f'word_rankings_for_{keyword}.json', 'w') as f:
        json.dump(all_original_rankings, f, indent=4)

    filtered_filename = f'filtered_word_rankings_for_{keyword}.txt'
    with open(filtered_filename, 'w') as f:
        for article_ranking in all_filtered_rankings:
            f.write(article_ranking)

    sorted_aggregate_rankings = sorted(word_ranking_sums.items(), key=lambda x: x[1])
    aggregated_filename = f'aggregated_rankings_for_{keyword}.txt'
    with open(aggregated_filename, 'w') as f:
        for i, (word, total_ranking) in enumerate(sorted_aggregate_rankings, start=1):
            f.write(f"{i}: {word} (Total Ranking: {total_ranking})\n")

    print(f"Processed '{keyword}'. Files saved: original, filtered, and aggregated rankings.")

def main():
    api_key = '286057e277b5469db123953b0e0d0214'
    keywords = ['Trump', 'Biden']
    total_rankings = []

    for keyword in keywords:
        process_keyword(api_key, keyword)  # Ensure this generates the aggregated rankings file
        aggregated_filename = f'aggregated_rankings_for_{keyword}.txt'
        top_rankings = read_top_aggregated_rankings(aggregated_filename, top_n=10)  # Adjust top_n as needed
        plot_keyword_rankings(top_rankings, keyword)

if __name__ == "__main__":
    main()