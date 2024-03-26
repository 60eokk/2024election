from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords_tfidf(documents, top_n=10):
    vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names_out()
    dense = tfidf_matrix.todense()
    denselist = dense.tolist()
    keywords = [sorted(zip(feature_names, doc), key=lambda x: x[1], reverse=True)[:top_n] for doc in denselist]
    return keywords



from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

def perform_lda(documents, n_topics=5, n_words=10):
    count_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    doc_term_matrix = count_vectorizer.fit_transform(documents)
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=0)
    lda.fit(doc_term_matrix)
    words = count_vectorizer.get_feature_names_out()
    topics = {i: [words[index] for index in topic.argsort()[:-n_words - 1:-1]] for i, topic in enumerate(lda.components_)}
    return topics




from textblob import TextBlob

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def analyze_subjectivity(text):
    analysis = TextBlob(text)
    return analysis.sentiment.subjectivity






# LIWC analysis typically requires proprietary software or datasets.
# This is a conceptual placeholder for how you might approach it if you had access to LIWC categories.
def analyze_liwc(text, liwc_categories):
    # Assume `liwc_categories` is a dict with keys as categories and values as lists of words in those categories.
    words = text.split()
    category_counts = {category: sum(word in words for word in word_list) for category, word_list in liwc_categories.items()}
    return category_counts
