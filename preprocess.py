import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_distances, pairwise_distances_chunked
from scipy.sparse import vstack
from nltk.corpus.reader.wordnet import NOUN
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


