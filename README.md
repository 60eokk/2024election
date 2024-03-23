"USEFUL TERMINAL COMMANDS":
1. which python
2. python --version
3. pip list 
4. python -m pip list: ##To ensure you're using the pip that corresponds to your python (or python3), you can explicitly call pip using Python with this##   (number3 and number4 should both have bs4. if one doesn't, it means they are in separate environments)
5. python -m pip install xxxxx


# 2024election

WHY:
I believe DATA "speaks".
Numbers, data have meaning, it is for us to figure out what they mean and how they correlate with each other.

Machine Learning is becoming big, maybe it is already too big. 
We use it to predict the future. 
So I wanted to take part in "predicting" the future by using data analysis, predicting the 2024 election

STEP BY STEP:
1) Which election will be used for analysis
2) Identify sources of articles, gossips
3) Python library (BeatifulSoup for scraping articles, Tweepy for social media posts, etc)
4) Archives / datasets related to past elections could help
5) Text cleaning (standarize format), remove (HTML tag, non alphanumeric characters, stop words)
6) Exploratory Data Analysis (keyword frequency, sentimment analysis, temporal trend, etc)
7) Perform correlation analysis
8) Machine learning model
9) Backtest and predict




1) 2020, 2016, 2012
2) TheNewYorkTimes, CNN, FOX News, Washington Post, Politicos, FiveThirtyEight, TheHill, RealClearPolitics, Breitbart for conservative perspectives and Daily Kos for liberal viewpoints, Reddit: Subreddits like r/politics, r/PoliticalDiscussion, and election-specific forums can be goldmines of public opinion and discussion, Twitter: Use hashtags related to the elections (e.g., #Election2020, #Trump2020, #Biden2020) (Or Twitter's Advanced Search), FB, YT, Pew Research Center and the Brookings Institution often conduct in-depth analysis and surveys on voter behavior and election trends, For older articles or content that has been removed, the Wayback Machine can help you access archived versions of web pages, 

First, start with "keywords", or frequently used phrases
Start with broad keywords, and then start narrowing down.

Keywords: Trump, Biden, Election, Win, Beat, Better, 
NEED TO SORT OUT THE RESULTS!, IT IS NOT ORGANIZED

Should I start making changes to this code to do more? or should I start making the same function for other websites?

# NEW METHOD!
instead of choosing the keywords by myself, I will check for all the keywords in the article related to presidents and then from there, list the keywords (most used) from top to bottom. THIS will be the keyword to election winner!

# RAN INTO MAJOR PROBLEM:
apparently, scraping data from sources like New York Times are is against policy... need to find another source!

#THUS
Other websites, for exameple: https://en.wikipedia.org/wiki/List_of_news_media_APIs
https://www.govtrack.us/
https://www.presidency.ucsb.edu/advanced-search?field-keywords=donald+trump&field-keywords2=&field-keywords3=&from%5Bdate%5D=&to%5Bdate%5D=&person2=&items_per_page=25


# ANOTHER PROBLEM:
NEWSAPI's free plan only gives 1 month old articles.

