# Approach to implement HuggingFace's NLP Models
# In order to so: Will do by starting over, and taking functions from main.py



# 1. data collection (collect articles from past)
# fetch and load articles --> will later be stored in csv/excel/sql
def fetch_articles(apikey, keyword, from_date, to_date, page_size):
    print(f"Fetching articles for '{keyword}' from {from_date} to {to_date}!")
    base_url = "https://content.guardianapis.com/search"
    params = {
        'api_key': apikey,
        'q': keyword,
        'page_size': page_size,
        'from-date': from_date,
        'to-date': to_date,
        'show-fields': body
    }


# 2. data processing (clean, process data)
# 3. use nlp models to extract features (sentiment scores, etc)
# 4. model training 
# 5. prediction