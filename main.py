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

stop_words = set(stopwords.words('english'))

def remove_spaces(lst):
    spaces_removed = []
    for name in lst:
        spaces_removed.append(name.replace(" ", ""))
    return spaces_removed

def list_for_remove(string):
    string=str(string)
    return " ".join(remove_spaces(string.split(", ")))

def clean_up(imdb_recomend,netflix_recommend):
    #fill any NAN values
    imdb_recomend.director.fillna("Unlisted")
    imdb_recomend.actors.fillna("Unavailable")
    imdb_recomend.genre.fillna("Unknown")
    netflix_recommend.listed_in.fillna("Unknown")
    netflix_recommend.director.fillna("Unlisted")
    netflix_recommend.cast.fillna("Unavailable")    
    
    #remove spaces from actors and directors names
    imdb_recomend["actors"] = imdb_recomend["actors"].apply(lambda x: list_for_remove(x))
    imdb_recomend["director"] = imdb_recomend["director"].apply(lambda x: list_for_remove(x))
    imdb_recomend["genre"] = imdb_recomend["genre"].apply(lambda x: list_for_remove(x))
    netflix_recommend["listed_in"] = netflix_recommend["listed_in"].apply(lambda x: list_for_remove(x))
    netflix_recommend["cast"] = netflix_recommend["cast"].apply(lambda x: list_for_remove(x))
    netflix_recommend["director"] = netflix_recommend["director"].apply(lambda x: list_for_remove(x))
    return imdb_recomend, netflix_recommend

def make_keywords(string):
    tokens = word_tokenize(string)
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation from each word
    import string
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    lem = WordNetLemmatizer()
    words = [lem.lemmatize(w) for w in words]
    return " ".join(words)

def get_keywords(imdb_recomend, netflix_recommend):
    imdb_recomend.description.fillna("Unknown",inplace=True) 
    netflix_recommend.description.fillna("Unknown",inplace=True) 
    imdb_recomend.description = imdb_recomend.description.apply(lambda x: make_keywords(x))
    netflix_recommend.description = netflix_recommend.description.apply(lambda x: make_keywords(x))
    return imdb_recomend, netflix_recommend

def mashup(imdb):
    str_list = []
    for i in range(imdb.shape[0]):
        key = imdb_recomend.description[i]+" "+(imdb_recomend.actors[i])+" "+(imdb_recomend.director[i])+" "+(imdb_recomend.genre[i])+" "+(imdb_recomend.year[i])
        str_list.append(key)
    return str_list

if __name__ == "__main__":
    print("Reading in files...")
    netflix = pd.read_csv("data/netflix_titles.csv")
    imdb_movies = pd.read_csv("data/IMDb movies.csv", low_memory=False)
    print("Done")
    netflix_recommend = netflix[["title",  "release_year","listed_in","director", "cast", "description"]]
    imdb_recomend = imdb_movies[["title", "year", "genre","director", "actors", "description"]]
    print("Cleaning files...")
    clean_imdb, clean_netflix = clean_up(imdb_recomend,netflix_recommend)
    cleaned_imdb, cleaned_netflix= get_keywords(clean_imdb, clean_netflix)
    print("Done")
    imdb_lst = mashup(cleaned_imdb)
    f = open("mashup.pkl", "w")
    pickle.dump(imdb_lst, f)
    f.close()

    vectorizor = CountVectorizer()
    keys = vectorizor.fit_transform(imdb_lst,y=cleaned_imdb.title)
    print("Attempting pairwise")
    distances = pairwise_distances(keys,metric='cosine')
    print("Done")
    stuff = np.argsort(distances[3])[0:11]
    print(cleaned_imdb.title[stuff])







