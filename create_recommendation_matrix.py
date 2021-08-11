import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_distances_chunked
from nltk.corpus.reader.wordnet import NOUN
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


def remove_spaces(lst):
    #remove spaces from items in list
    spaces_removed = []
    for name in lst:
        spaces_removed.append(name.replace(" ", ""))
    return spaces_removed

def list_for_remove(string):
    #split on items and send list of items to have spaces removed
    string=str(string)
    return " ".join(remove_spaces(string.split(", ")))

def clean_up(pd_df):
    #fill any NAN values
    pd_df =pd_df.copy()
    #remove spaces from actors and directors names as well as genres
    pd_df.actors = pd_df.actors.apply(lambda x: list_for_remove(x))
    pd_df.director = pd_df.director.apply(lambda x: list_for_remove(x))
    pd_df.genre = pd_df.genre.apply(lambda x: list_for_remove(x))
    return pd_df        


def get_keywords(pd_df):
    #reduce titles and descriptions to keywords
    pd_df = pd_df.copy()
    pd_df.description = pd_df.description.apply(lambda x: make_keywords(x, dis=True))
    pd_df.original_title = pd_df.original_title.apply(lambda x: make_keywords(x))
    return pd_df

def make_keywords(string,dis=False):

    
    # convert to lower case
    tokens = word_tokenize(string)
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
    if not dis:
        stop_words = set(stopwords.words(['arabic', 'azerbaijani', 'danish', 'dutch', 'english', 'finnish', 'french', 'german', 'greek','hungarian', 'indonesian', 'italian', 'kazakh', 'nepali', 'norwegian', 'portuguese', 'romanian', 'russian', 'slovene', 'spanish', 'swedish', 'tajik', 'turkish']))
    words = [w for w in words if not w in stop_words]

    # lemmatize remaining words
    lem = WordNetLemmatizer()
    words = [lem.lemmatize(w) for w in words]
    return " ".join(words)

#trans13
def mashup(pd_df):
    str_list = []
    # set defaults in case of NAN
    key = ''
    direct = ' '
    act = ' '
    descrip = ' '
    original = ' '

    # adjust weights for features ignore NANs
    for i in range(pd_df.shape[0]):
        if i not in pd_df.index:
            continue
        # weight description 
        if 'NAN' not in pd_df.description[i]:
            descrip = (pd_df.description[i] + " ") * 3
        # weight first actor
        if 'NAN' not in pd_df.actors[i]:
            act = (pd_df.actors[i].split()[0] + " ") * 6
            #If second actor then weight accordingly
            if len(pd_df.actors[i].split())>2:
                act = act + (pd_df.actors[i].split()[1] + " ") * 5
            #if additional actors weight by last scale
            if len(pd_df.actors[i].split())>2:
                act = act + ((" ".join(pd_df.actors[i].split()[2:]) + " ") * 4)
        #weight director name
        if 'NAN' not in pd_df.director[i]:
            direct = (pd_df.director[i] + " ") * 6
        # weight title
        if 'NAN' not in pd_df.original_title[i]:
            original = (pd_df.original_title[i] + " ") * 5
        # combine all weighted sections with the weighted genre section
        key = direct + " " + act + " " + descrip + " " + original + ((pd_df.genre[i] + " ")*3)
        # append weighted word list for title to corpus list
        str_list.append(key)
    return str_list

def make_matrix(dist, total):
    y=0
    while (y < total.shape[0]):
        pull = next(dist)
        if y == 0:
            save = pull.shape[0]
        y += pull.shape[0]
        dbfile = open(f'distance/translated13_weights_full_set{y}.pkl', 'ab')
        # source, destination
        pickle.dump(pull, dbfile)                     
        dbfile.close()
    return save

if __name__ == "__main__":
    # read in combined dataframe with description translated
    total = pd.read_csv('translated_in_case.csv', low_memory=False)
    total.drop('Unnamed: 0', axis=1, inplace=True)
    total.fillna("NAN",inplace=True)

    # clean up text and get word lists
    total = clean_up(total)
    total = get_keywords(total)
    total.fillna("NAN",inplace=True)
    total_lst = mashup(total)

    # process word lists into vectors and get saved distance files
    vectorizor = CountVectorizer()
    keys = vectorizor.fit_transform(total_lst)
    dist = pairwise_distances_chunked(keys, metric='cosine')
    save = make_matrix(dist, total)


