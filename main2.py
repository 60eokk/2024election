# Approach to implement HuggingFace's NLP Models
# In order to so: Will do by starting over, and taking functions from main.py

import requests
# from theguardian import theguardian_content
from bs4 import BeautifulSoup



# 1. data collection (collect articles from past)
# fetch and load articles --> will later be stored in csv/excel/sql
def fetch_articles(apikey, keyword, from_date, to_date, page_size):
    print(f"Fetching articles for '{keyword}' from {from_date} to {to_date}!")
    url = "https://content.guardianapis.com/search"
    params = {
        'api-key': apikey,
        'q': keyword,
        'page-size': page_size, 
        'from-date': from_date,
        'to-date': to_date,
        'show-fields': 'body'
    }

    response = requests.get(url, params = params)

    if response.status_code == 200:
        print(response.json())
    else:
        print("error")


# can this be done without clean_html
def clean_data(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    return soup.get_text()



def main():
    apikey = '2ce72283-ccba-4b1a-92da-2f702366b61c'

    # test case
    keyword, from_date, to_date, page_size = "Trump", '2020-01-01', '2020-12-31', '2'
    fetch_articles(apikey, keyword, from_date, to_date, page_size)
    clean_data(fetch_articles)


if __name__ == "__main__":
    main()

#




# 2. data processing (clean, process data)
# 3. use nlp models to extract features (sentiment scores, etc)
# 4. model training 
# 5. prediction