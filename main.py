# NEWSAPI usage below

from newsapi import NewsApiClient

# Initialize the client with your API key
api_key = '286057e277b5469db123953b0e0d0214'
api = NewsApiClient(api_key=api_key)

# Fetch top headlines using the keyword "Trump"
keyword = 'Trump'
top_headlines = api.get_everything(q=keyword)

# Check if the request was successful
if top_headlines['status'] == 'ok':
    # Iterate through the articles and print details
    for article in top_headlines['articles']:
        source = article['source']['name']
        title = article['title']
        description = article['description']
        print(f"Source: {source}\nTitle: {title}\nDescription: {description}\n")
else:
    print("Failed to fetch top headlines.")

