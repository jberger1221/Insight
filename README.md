# Insight Project

<img src="https://github.com/jberger1221/Insight/blob/master/streamlitapp/Logo.png" width="100">

## Fertile Crescent (fertilecrescent.xyz)


Finding the right clinic is difficult and takes a lot of time. There are thousands of reviews to read which takes more time read than people have. Fertile Crescent is a Webapp that helps makes the research process simpler and quicker, allowing a user to find summaries for reviews by clininc, by review topic and by review sentiment. Additionally, Ferticle Crescent also uses CDC data to plot historical success rates for each clinic, data not easily available on any other site.

Fertile Crescent uses a combination of natural languange process techniques to clean scraped data, classify reviews into topics and summarize the reviews. More specifically, Ferticle Crescent scrapes reviews using beautiful soup and selenium. The reviews are cleaned using gensim. A model is trained using data from fertility_iq and used to classify unstructered yelp reviews. The modeling is built using different types of word embeddings with a variety of classification models. The model with the best performance uses word2vec, with a pre-trained google news embedding, to vectorize the word embeddings with a support vector machine. The sentiment of each review is scored using Vader sentiment analysis. Finally the summary is built using the BERT extractive summarizer using the small English spaCy model.

## The Front Page of Fertile Crescent
<img src="https://github.com/jberger1221/Insight/blob/master/streamlitapp/Screen Shot 2020-07-09 at 10.31.44 AM.png" width="1000">

## Fertile Crescent Use Case after selecting review source.
<img src="https://github.com/jberger1221/Insight/blob/master/streamlitapp/Screen Shot 2020-07-09 at 10.32.26 AM.png" width="1000"> 
