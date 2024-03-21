### USING BLOOMBERG API
# BLOOMBERG API IS DIFFERENT: It does not require API KEY.
# Bloomberg API access is typically granted through licensed software like the Bloomberg Terminal or Server API (SAPI)

import blpapi
from datetime import datetime

def main():
    # Initialize the session options with the Bloomberg service
    sessionOptions = blpapi.SessionOptions()
    sessionOptions.setServerHost('localhost')
    sessionOptions.setServerPort(8194)

    # Create and start a session
    session = blpapi.Session(sessionOptions)
    if not session.start():
        print("Failed to start session.")
        return

    # Open the news service (this is a placeholder; actual service endpoint may vary)
    if not session.openService("//blp/news_service"):
        print("Failed to open news service.")
        return

    # Obtain the service
    newsService = session.getService("//blp/news_service")
    
    # Create a request for news data (Note: The actual request type and parameters depend on Bloomberg's API)
    request = newsService.createRequest("NewsSearchRequest")  # This is hypothetical and for illustrative purposes
    request.set("query", "Trump")  # Assuming there's a way to set a query or keywords
    # Set additional request parameters if necessary, such as date range or news source filters

    # Send the request
    print("Sending request for news about 'Trump'...")
    session.sendRequest(request)

    # Process the incoming events/messages
    while True:
        event = session.nextEvent()
        for msg in event:
            # Here, you would parse the msg to extract and process news information
            print(msg)
        if event.eventType() in (blpapi.Event.RESPONSE, blpapi.Event.PARTIAL_RESPONSE):
            break
        elif event.eventType() == blpapi.Event.SESSION_STATUS:
            if msg.messageType() == blpapi.Name("SessionTerminated"):
                print("Session terminated")
                return

if __name__ == "__main__":
    main()





##### BELOW IS THE CODE FOR THE NEW YORK TIMES

# import requests
# import json
# from collections import Counter
# import re

# def count_words(text):
#     # Remove punctuation and split text into words
#     words = re.findall(r'\b\w+\b', text.lower())
#     # Count each word
#     word_counts = Counter(words)
#     # Return the most common words and their counts
#     return word_counts.most_common()



# # Feature 5: Interactive User Input
# keywords = input("Enter keywords separated by 'OR': ")
# begin_date = input("Enter start date (YYYYMMDD): ")
# end_date = input("Enter end date (YYYYMMDD): ")
# api_key = '1ffP4T6741HAX9gA7xVs2XkY6aYX79wH'

# print("Searching for articles with keywords: ", keywords)

# # Constructing the URL with date range and combined keywords
# url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={keywords}&begin_date={begin_date}&end_date={end_date}&api-key={api_key}'

# try:
#     response = requests.get(url)
    
#     # Feature 3: Error Handling
#     response.raise_for_status()  # This will raise an exception for HTTP errors
    
#     articles = response.json()
    
#     # Feature 4: Saving Results to File
#     with open('articles.json', 'w') as f:
#         json.dump(articles, f, indent=4)
    
#     # Process the articles and count words in snippets
#     for i, doc in enumerate(articles['response']['docs']):
#         headline = doc['headline']['main']
#         article_url = doc['web_url']
#         print(f"Title: {headline}\nURL: {article_url}\n")
        
#         # Use snippet as example text; replace with full text if available
#         text = doc.get('snippet', '')
#         if text:
#             word_rankings = count_words(text)
#             # Save word rankings to a separate file for each article
#             ranking_filename = f'word_ranking_{i}.json'
#             with open(ranking_filename, 'w') as f:
#                 json.dump(word_rankings, f, indent=4)
#             print(f"Word rankings saved to {ranking_filename}")

# except requests.exceptions.HTTPError as http_err:
#     print(f"HTTP error occurred: {http_err}")
# except Exception as err:
#     print(f"An error occurred: {err}")


# # TWO DOCUMENTATION PAGES
# #https://api.ap.org/media/v/docs/#t=Pricing.htm
# # https://bloomberg.github.io/blpapi-docs/python/3.23/