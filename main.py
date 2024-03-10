


import requests

api_key = '1ffP4T6741HAX9gA7xVs2XkY6aYX79wH'
keyword = 'election'

# Constructing the URL for the API request
url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={keyword}&api-key={api_key}'

# Making the GET request to the New York Times Article Search API
response = requests.get(url)
# response = requests.get("https://api.nytimes.com/svc/search/v2/articlesearch.json?q=election&api-key=1ffP4T6741HAX9gA7xVs2XkY6aYX79wH")


print("Status Code:", response.status_code)
print("Response:", response.text)
print("hi")


# # Checking if the request was successful
# if response.status_code == 200:
#     # Convert the response to JSON
#     articles = response.json()
    
#     # Example: Print out the headline of the first article
#     first_article_headline = articles['response']['docs'][0]['headline']['main']
#     print(f"First article headline: {first_article_headline}")
# else:
#     print("Failed to fetch articles")


