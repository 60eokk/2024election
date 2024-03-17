import requests
import json

# Feature 5: Interactive User Input
keywords = input("Enter keywords separated by 'OR': ")
begin_date = input("Enter start date (YYYYMMDD): ")
end_date = input("Enter end date (YYYYMMDD): ")
api_key = '1ffP4T6741HAX9gA7xVs2XkY6aYX79wH'

print("Searching for articles with keywords: ", keywords)

# Constructing the URL with date range and combined keywords
url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={keywords}&begin_date={begin_date}&end_date={end_date}&api-key={api_key}'

try:
    response = requests.get(url)
    
    # Feature 3: Error Handling
    response.raise_for_status()  # This will raise an exception for HTTP errors
    
    articles = response.json()
    
    # Feature 4: Saving Results to File
    with open('articles.json', 'w') as f:
        json.dump(articles, f, indent=4)
    
    # Process the articles
    for doc in articles['response']['docs']:
        headline = doc['headline']['main']
        article_url = doc['web_url']
        print(f"Title: {headline}\nURL: {article_url}\n")

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"An error occurred: {err}")


# FUTURE REFERENCE URL
# https://www.270towin.com/historical-presidential-elections/
