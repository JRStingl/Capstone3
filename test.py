import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_distances
from scipy.sparse import vstack
from nltk.corpus.reader.wordnet import NOUN
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string


if __name__ == "__main__":
    dbfile = open("mashup.pkl", 'rb')  
    imdb_lst = pickle.load(dbfile)
    dbfile.close()
    cleaned_imdb = pd.read_csv("small_title.csv")

    vectorizor = CountVectorizer()
    keys = vectorizor.fit_transform(imdb_lst,y=cleaned_imdb.title)
    print("Attempting pairwise")
    distances = pairwise_distances(keys,metric='cosine')
    print("Done")
    stuff = np.argsort(distances[3])[0:11]
    print(cleaned_imdb.title[stuff])