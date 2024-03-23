# another version of NEWSAPI


from newsapi import NewsApiClient
from collections import Counter
import re
import json
import requests
from bs4 import BeautifulSoup

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

def main():
    api_key = '286057e277b5469db123953b0e0d0214'
    api = NewsApiClient(api_key=api_key)
    keyword = 'Trump'

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
        
        # Keep original rankings
        all_original_rankings.append({
            'title': title,
            'url': url,
            'word_rankings': ranked_words[:10]
        })

        # Filter out stop words for the new rankings
        filtered_rankings = [(word, count) for word, count in ranked_words if word not in stop_words][:10]
        formatted_filtered_rankings = f"Article {index}: {title}\nURL: {url}\nTop words:\n" + \
                            '\n'.join([f"{i+1}: {word} ({count} times)" for i, (word, count) in enumerate(filtered_rankings)]) + \
                            "\n\n"
        all_filtered_rankings.append(formatted_filtered_rankings)
        
        # Sum the rankings for aggregate scoring
        for i, (word, _) in enumerate(filtered_rankings):
            if word not in word_ranking_sums:
                word_ranking_sums[word] = 0
            word_ranking_sums[word] += (i + 1)  # Add the ranking to the sum

    # Save original rankings to JSON file
    with open(f'word_rankings_for_{keyword}.json', 'w') as f:
        json.dump(all_original_rankings, f, indent=4)

    # Save new filtered rankings to a separate text file
    filtered_filename = f'filtered_word_rankings_for_{keyword}.txt'
    with open(filtered_filename, 'w') as f:
        for article_ranking in all_filtered_rankings:
            f.write(article_ranking)
            
    # Sort words by their aggregated ranking sums, from smallest to largest
    sorted_aggregate_rankings = sorted(word_ranking_sums.items(), key=lambda x: x[1])
    
    # Save the aggregated rankings to a new file
    aggregated_filename = f'aggregated_rankings_for_{keyword}.txt'
    with open(aggregated_filename, 'w') as f:
        for i, (word, total_ranking) in enumerate(sorted_aggregate_rankings, start=1):
            f.write(f"{i}: {word} (Total Ranking: {total_ranking})\n")

    print(f"Original word rankings for all articles related to '{keyword}' have been saved to 'word_rankings_for_{keyword}.json'.")
    print(f"Filtered word rankings for all articles related to '{keyword}' have been saved to '{filtered_filename}'.")
    print(f"Aggregated word rankings across all articles have been saved to '{aggregated_filename}'.")

if __name__ == "__main__":
    main()

