# NLTK Word Handling
import re
from collections import Counter
from nltk.corpus import stopwords
import nltk

# Make sure to download the stopwords dataset from NLTK
nltk.download('stopwords')

def count_words(text):
    """Count words in a text, excluding common stop words."""
    stop_words = set(stopwords.words('english'))
    # Extend the stop words list with custom words specific to your dataset
    custom_stop_words = ["https", "com", "theguardian", "href", "www"]
    stop_words.update(custom_stop_words)
    
    words = re.findall(r'\b\w+\b', text.lower())
    filtered_words = [word for word in words if word not in stop_words and len(word) > 1]
    return Counter(filtered_words)




# Plotfly Interactive Visualization
import plotly.express as px

def plot_keyword_rankings_interactive(rankings, keyword):
    """Plot an interactive bar graph of the top word rankings for a given keyword using Plotly."""
    if rankings:
        words, scores = zip(*rankings)
        fig = px.bar(x=words, y=scores, labels={'x':'Words', 'y':'Frequency'}, title=f'Top Word Rankings for {keyword}')
        fig.show()
    else:
        print(f"No data to plot for '{keyword}'.")

# Example usage with dummy data
rankings = [('election', 50), ('vote', 45), ('policy', 30)]
plot_keyword_rankings_interactive(rankings, 'Example Keyword')



# Sentiment Analysis
from textblob import TextBlob

def analyze_sentiment(text):
    """Analyze the sentiment of a text and return it."""
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity  # Returns a value between -1 (negative) and 1 (positive)
    return sentiment

def aggregate_article_sentiments(articles):
    """Aggregate sentiments of a list of articles, returning the average sentiment."""
    total_sentiment = 0
    for title, body in articles:
        sentiment = analyze_sentiment(body)
        print(f"Sentiment for '{title}': {sentiment}")
        total_sentiment += sentiment
    average_sentiment = total_sentiment / len(articles) if articles else 0
    print(f"Average Sentiment: {average_sentiment}")
    return average_sentiment

# Example usage
articles = [("Title 1", "This is a great day for democracy."), ("Title 2", "This is a sad day for democracy.")]
aggregate_article_sentiments(articles)