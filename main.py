import requests
import webbrowser

api_key = '1ffP4T6741HAX9gA7xVs2XkY6aYX79wH'
# Combine keywords with "OR" for the query
keywords = 'Trump OR Biden OR Election OR Win OR Beat OR Better'
begin_date = '20200101'  # Example start date: January 1, 2020
end_date = '20201231'    # Example end date: December 31, 2020

print("Searching for articles with keywords: ", keywords)

# Constructing the URL with date range and combined keywords
url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={keywords}&begin_date={begin_date}&end_date={end_date}&api-key={api_key}'

response = requests.get(url)

if response.status_code == 200:
    articles = response.json()
    
    # Set a limit to how many URLs to open to avoid overwhelming the browser
    open_limit = 5
    opened_count = 0

    # Iterate over articles in the response
    for doc in articles['response']['docs']:
        headline = doc['headline']['main']
        article_url = doc['web_url']
        print(f"Title: {headline}\nURL: {article_url}\n")
        
        # Automatically open the article URL in the default browser, with a limit
        if opened_count < open_limit:
            webbrowser.open(article_url)
            opened_count += 1
else:
    print(f"Failed to fetch articles. Status Code: {response.status_code}")
    print("Response:", response.text)


# import requests

# api_key = '1ffP4T6741HAX9gA7xVs2XkY6aYX79wH'
# keyword = 'election'
# begin_date = '20200101'  # Example start date: January 1, 2020
# end_date = '20201231'    # Example end date: December 31, 2020


# print ("NEXT KEYWORD: ", keyword)

# # Constructing the URL with date range
# url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={keyword}&begin_date={begin_date}&end_date={end_date}&api-key={api_key}'

# response = requests.get(url)

# if response.status_code == 200:
#     articles = response.json()
    
#     # Iterate over articles in the response
#     for doc in articles['response']['docs']:
#         headline = doc['headline']['main']
#         url = doc['web_url']
#         print(f"Title: {headline}\nURL: {url}\n")
# else:
#     print(f"Failed to fetch articles. Status Code: {response.status_code}")
#     print("Response:", response.text)





# keyword = 'Trump'
# print ("NEXT KEYWORD: ", keyword)

# url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={keyword}&begin_date={begin_date}&end_date={end_date}&api-key={api_key}'

# response = requests.get(url)

# if response.status_code == 200:
#     articles = response.json()\
    
#     # Iterate over articles in the response
#     for doc in articles['response']['docs']:
#         headline = doc['headline']['main']
#         url = doc['web_url']
#         print(f"Title: {headline}\nURL: {url}\n")
# else:
#     print(f"Failed to fetch articles. Status Code: {response.status_code}")
#     print("Response:", response.text)