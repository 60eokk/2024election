import requests
from collections import Counter
import re
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import plotly.express as px
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
# Added imports for LDA
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

# Ensure NLTK resources are downloaded
nltk.download('stopwords')

def fetch_articles(api_key, keyword, page_size):
    print(f"Fetching articles for '{keyword}'...")
    base_url = "https://content.guardianapis.com/search"
    params = {
        'api-key': api_key,
        'q': keyword,
        'page-size': page_size,
        'show-fields': 'body',
        'from-date': '2012-01-01',
        'to-date': '2012-12-31'
    }
    constructed_url = requests.Request('GET', base_url, params=params).prepare().url
    print(f"Constructed URL for '{keyword}': {constructed_url}")
   
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

def count_words(text):
    stop_words = set(stopwords.words('english'))
    custom_stop_words = ["https", "com", "theguardian", "href", "www", "class", "block", "time", "div", "id", "h2", "figure", "elements"]
    stop_words.update(custom_stop_words)
    
    words = re.findall(r'\b\w+\b', text.lower())
    filtered_words = [word for word in words if word not in stop_words and len(word) > 1]
    return Counter(filtered_words)

def extract_keywords_tfidf(documents, top_n=10):
    vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names_out()
    dense = tfidf_matrix.todense().tolist()
    keywords = [sorted(zip(feature_names, doc), key=lambda x: x[1], reverse=True)[:top_n] for doc in dense]
    return keywords

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def perform_lda(documents, n_topics=5, n_words=10):
    count_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    doc_term_matrix = count_vectorizer.fit_transform(documents)
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=0)
    lda.fit(doc_term_matrix)
    words = count_vectorizer.get_feature_names_out()
    topics = {i: [words[index] for index in topic.argsort()[:-n_words - 1:-1]] for i, topic in enumerate(lda.components_)}
    return topics

def aggregate_rankings(articles, keyword):
    print(f"Aggregating rankings for {len(articles)} articles...")
    word_ranking_sums = Counter()
    sentiments = []
    for title, body in articles:
        word_counts = count_words(body)
        word_ranking_sums.update(word_counts)
        sentiment = analyze_sentiment(body)
        sentiments.append(sentiment)
    average_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
    print(f"Average sentiment for '{keyword}': {average_sentiment}")
    return word_ranking_sums.most_common(20), average_sentiment

def plot_keyword_rankings_interactive(rankings, keyword):
    if rankings:
        words, scores = zip(*rankings)
        fig = px.bar(x=words, y=scores, title=f'Top Word Rankings for {keyword}', labels={'x':'Words', 'y':'Frequency'})
        fig.show()
    else:
        print(f"No data to plot for '{keyword}'.")

def main():
    api_key = '2ce72283-ccba-4b1a-92da-2f702366b61c' 
    keywords = ['Obama', 'Romney']
    for keyword in keywords:
        articles = fetch_articles(api_key, keyword, page_size=50)
        if articles:
            article_bodies = [body for _, body in articles]
            tfidf_keywords = extract_keywords_tfidf(article_bodies)
            print(f"TF-IDF Keywords for {keyword}: {tfidf_keywords[0]}")  # Showing keywords for the first article for brevity
            
            lda_topics = perform_lda(article_bodies)
            print(f"LDA Topics for {keyword}: {lda_topics}")

            rankings, average_sentiment = aggregate_rankings(articles, keyword)
            plot_keyword_rankings_interactive(rankings, keyword)
        else:
            print(f"No articles fetched for '{keyword}', skipping plotting.")

if __name__ == "__main__":
    main()
