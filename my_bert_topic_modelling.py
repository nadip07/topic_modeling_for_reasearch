# -*- coding: utf-8 -*-
"""MY_BERT_Topic_Modelling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IahGqdx4uJwmqqeVc1ghG3JdNvT_r-7v

# **BERTopic - Tutorial**
"""

!pip install bertopic[visualization] --quiet

"""# **Imports**"""

import numpy as np
import pandas as pd
from copy import deepcopy
from bertopic import BERTopic

import re
import nltk
import spacy
import string
pd.options.mode.chained_assignment = None

nltk.download('wordnet')
nltk.download('omw-1.4')

"""# **Load data**"""

df = pd.read_csv("/content/data_amazon (8).csv")

df=df.dropna(subset=['Review', 'Materials', 'Construction', 'Color', 'Finishing', 'Durability'])

df =df.drop(["Title", "Materials", "Construction", "Color", "Finishing", "Durability", "Cons_rating", "Cloth_class"], axis = 1)

df.head()

df['Review']=df['Review'].str.lower()
df.head(150)

PUNCT_TO_REMOVE = string.punctuation
def remove_punctuation(text):
    """custom function to remove the punctuation"""
    return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))

df["Review"] = df["Review"].apply(lambda text: remove_punctuation(text))
df.head()

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
", ".join(stopwords.words('english'))

STOPWORDS = set(stopwords.words('english'))
def remove_stopwords(text):
    """custom function to remove the stopwords"""
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])

df["Review"] = df["Review"].apply(lambda text: remove_stopwords(text))
df.head(50)

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

df["Review"] = df["Review"].apply(lambda text: remove_emoji(text))
df.head(200)

from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
def lemmatize_words(text):
    return " ".join([lemmatizer.lemmatize(word) for word in text.split()])

df["Review"] = df["Review"].apply(lambda text: lemmatize_words(text))
df.head(200)

from collections import Counter
cnt = Counter()
for text in df["Review"].values:
    for word in text.split():
        cnt[word] += 1
        
cnt.most_common(10)

FREQWORDS = set([w for (w, wc) in cnt.most_common(10)])
def remove_freqwords(text):
    """custom function to remove the frequent words"""
    return " ".join([word for word in str(text).split() if word not in FREQWORDS])

df["Review"] = df["Review"].apply(lambda text: remove_freqwords(text))
df.head()

docs = list(df.loc[:, "Review"].values)

"""# **Creating Topics**"""

from sentence_transformers import SentenceTransformer

sentence_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
embeddings = sentence_model.encode(docs, show_progress_bar=True)

model = BERTopic("bert-large-uncased",  calculate_probabilities=True)

topics, probs = model.fit_transform(docs, embeddings )

"""# We can then extract most frequent topics:"""

model.get_topic_freq()

"""# Get Individual Topics"""

model.get_topic(0)

model.get_topic(1)

model.get_topic(2)

model.get_topic(3)

model.get_topic(4)

model.get_topic(5)

model.get_topic(6)

model.get_topic(7)

model.get_topic(8)

model.get_topic(9)

model.reduce_topics(docs, nr_topics=10)

model.get_representative_docs(0)

model.get_representative_docs(1)

model.get_representative_docs(2)

model.get_representative_docs(3)

model.get_representative_docs(4)

model.get_representative_docs(5)

model.get_representative_docs(6)

model.get_representative_docs(7)

model.get_representative_docs(8)

model.get_representative_docs(9)

"""# **Visualize Topics**"""

model.visualize_topics(top_n_topics = 10)

model.visualize_hierarchy(top_n_topics=10)

model.visualize_barchart(top_n_topics=10)

model.visualize_heatmap(top_n_topics=10)

# Visualize probability distribution
model.visualize_distribution(model.probabilities_[1], min_probability=0.015)

# Get the topic predictions
topic_prediction = model.topics_[:]

# Save the predictions in the dataframe
df['topic_prediction'] = topic_prediction

# Take a look at the data
df

