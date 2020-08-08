#!/usr/bin/env python
# coding: utf-8

# # Data Cleaning

# ## Introduction

# Varibles such as stress and motivation can have both positive and negative affective states on performers.  Subsequently players are asked to submit a tweet-length assessment of their physical, mental and emotiona status in their own words.  What I'm looking for are signs of burnout - where sentiment might change from positive or negative or from fact based to opinion based, and vice versa.   It's important not to assume positive sentiment correlates with burnout. what we're looking for are significant changes in personality as expressed in sentiment.  Burnout is associated with the CHANGE not the affective state of the change; 
# 
# Secondly, if there is a change, it can give us a better understaning around the persoal motivational constructs and goal orientation of the athlete.  
# 
# 1. **Get 'Tweet' from database
# 2. **Clean the text
# 3. **Organizing the data
# 4. **Render as JSON for easier charting/graphing. 
# 
# The output of this notebook will render two JSON routes
# 
# 1. **tweet** - a collection of text
# 2. **Document-Term Matrix** - word counts in matrix format to run word count on

# In[28]:


#pull the data
import pandas as pd
data = pd.read_csv('derby_scored.csv')
data.head()


# In[29]:


#Get Essential data only
import pandas as pd
#pd.set_option('max_colwidth',150)

#data_df = pd.DataFrame.from_dict(data_combined).transpose()
data_df = data[['timestamp','player','tweet']]
data_df = data_df.sort_index()
data_df


# In[30]:


# Apply a first round of text cleaning techniques
import re
import string

def clean_text_round1(text):
    '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text

round1 = lambda x: clean_text_round1(x)


# In[31]:


# Let's take a look at the updated text
data_clean = pd.DataFrame(data_df.tweet.apply(round1))
data_clean


# In[32]:


# Apply a second round of cleaning
def clean_text_round2(text):
    '''Get rid of some additional punctuation and non-sensical text that was missed the first time around.'''
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    return text

round2 = lambda x: clean_text_round2(x)


# In[33]:


# Let's take a look at the updated text
data_clean = pd.DataFrame(data_clean.tweet.apply(round2))
data_clean["player"] = data_df["player"]
data_clean


# ## Organizing The Data

# The output of this notebook will be in two standard text formats:
# 1. **tweets - **a collection of text
# 2. **Document-Term Matrix - **word counts in matrix format

# In[22]:


# Let's pickle it for later use
data_clean.to_pickle("tweet.pkl")


# ### Document-Term Matrix

# For the next analysis the text must be tokenizedinto smaller pieces. Breaking down text into words is a common tokenization technique. We can use scikit-learn's CountVectorizer. 
# 
# CountVectorizer can also remove stop words. Stop words are common words that add no additional meaning to text such as 'a', 'the', etc.

# In[34]:


# We are going to create a document-term matrix using CountVectorizer, and exclude common English stop words
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(stop_words='english')
data_cv = cv.fit_transform(data_clean.tweet)
data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
data_dtm.index = data_clean.index
data_dtm


# In[37]:


# Let's pickle it for later use
data_dtm.to_pickle("dtm.pkl")
data_dtm.to_csv("dtm.csv")


# In[38]:


import pickle
# Let's also pickle the cleaned data (before we put it in document-term matrix format) and the CountVectorizer object
data_clean.to_pickle('data_clean.pkl')
data_clean.to_csv('data_clean.csv')
pickle.dump(cv, open("cv.pkl", "wb"))

