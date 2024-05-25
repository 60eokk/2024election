"USEFUL TERMINAL COMMANDS":
1. which python
2. python --version
3. pip list 
4. python -m pip list: To ensure you're using the pip that corresponds to your python (or python3), you can explicitly call pip using Python with this   (number3 and number4 should both have bs4. if one doesn't, it means they are in separate environments)
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



# Variables
- Years I will be Using: 2020, 2016, 2012
- Possible API Sources: 
    - TheNewYorkTimes, CNN, FOX News, Washington Post, Politicos, FiveThirtyEight, TheHill, RealClearPolitics,
    - Breitbart for conservative perspectives and Daily Kos for liberal viewpoints, 
    - Reddit: Subreddits like r/politics, r/PoliticalDiscussion, and election-specific forums can be goldmines of public opinion and discussion,
    - Twitter: Use hashtags related to the elections (e.g., #Election2020, #Trump2020, #Biden2020) (Or Twitter's Advanced Search), 
    - Pew Research Center and the Brookings Institution often conduct in-depth analysis and surveys on voter behavior and election trends
    - For older articles or content that has been removed, the Wayback Machine can help you access archived versions of web pages, 

# Steps
1. Start with "keywords", or frequently used phrases
2. Start with broad keywords, and then start narrowing down.
3. Keywords: Trump, Biden, Election, Win, Beat, Better (NEED TO SORT OUT THE RESULTS!, IT IS NOT ORGANIZED)


# NEW METHOD!
Instead of choosing the keywords by myself, I will check for all the keywords in the article related to presidents and then from there, list the keywords (most used) from top to bottom. THIS will be the keyword to election winner!


## RAN INTO PROBLEM:
Scraping data from sources like New York Times are is against policy... need to find another source!

Other websites, for example: 
- https://en.wikipedia.org/wiki/List_of_news_media_APIs
- https://www.govtrack.us/
- https://www.presidency.ucsb.edu/advanced-search?field-keywords=donald+trump&field-keywords2=&field-keywords3=&from%5Bdate%5D=to%5Bdate%5D=&person2=&items_per_page=25


## ANOTHER PROBLEM:
NEWSAPI's free plan only gives 1 month old articles


# VISUALIZATION & RESULTS
https://docs.google.com/document/d/1O4LLFkadXbtYKDyWrAESpWI6goYGWNZUTmyFYXvSvSM/edit
- Changes to docs 
- Trying to use other methods and added to docs

# Currently making the way to document the results
- LDA Method:
- "topic modeling" (which is more than just TF-IDF method that have been focusing only on frequently used words)


# How can I make it a better code?
- Refinement of Data Preprocessing:
Improve text cleaning to remove non-relevant words (HTML tags, common words) more effectively.

Implement lemmatization to consolidate different forms of the same word into a single term (e.g., "running" and "ran" to "run").

- Advanced Text Analysis:
Apply Named Entity Recognition (NER) to identify and compare the prominence of people, organizations, and locations mentioned alongside each candidate.

Utilize part-of-speech tagging to understand the context in which certain words are used.

- Sentiment Analysis Over Time:
Conduct a time-series analysis of sentiment associated with each candidate.

Compare the sentiment trend with key events during the campaign to see if there's a correlation.

- Topic Modeling:
Perform Latent Dirichlet Allocation (LDA) or Non-Negative Matrix Factorization (NMF) to discover topics within the articles.

Analyze the evolution of topics over time and compare the focus areas between different candidates.

- Predictive Modeling:
Build a model to predict election outcomes based on news article analysis. Compare the model's predictions with actual historical outcomes.

- User Interface:
Develop a web application that allows users to enter a candidate's name and get a visual representation of the analysis.

Provide interactive visualizations that users can engage with to explore the data further.

- Comparative Analysis:
Expand the dataset to include articles from multiple news sources to compare the representation of candidates across the media spectrum.

Analyze the differences in language used by different political affiliations or news outlets.

- Data Visualization:
Use more advanced visualization tools (like D3.js) for creating interactive and engaging data presentations.

Implement dashboards that provide insights at a glance.

- Data Collection Expansion:
Incorporate social media data to gauge public sentiment and compare it with the media portrayal.

Use APIs from Twitter, Reddit, or other platforms for a more comprehensive analysis.

- Documentation and Reporting:
Write detailed documentation about your methodology, data sources, and findings.

Create a report or a series of blog posts that narrate the story your data tells.

- Code Quality:
Refactor the code to improve readability and maintainability.

Write unit tests to ensure that each part of your codebase works correctly after changes.