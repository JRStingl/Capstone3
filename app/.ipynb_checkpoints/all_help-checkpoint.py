import pandas as pd
import pickle
import numpy as np
from flask import Flask, Response, render_template, request, redirect
from urllib.parse import urlencode, urlparse, parse_qs
from lxml.html import fromstring
from requests import get


def get_pickle(imdbid, imdb_movies):
    # takes in the id for the title and the dataframe
    # returns distance matrix and index
    ind = imdb_movies[imdb_movies.title_id==imdbid].index[0]
    lst = []
    for i in range(1,100):
        lst.append((i*1433)-1)
    for i in range(len(lst)):
        if ind < lst[i]:
            files = (lst[i])+1
            break
    dbfile = open(f'../distance/translated13_weights_full_set{int(files)}.pkl', 'rb')
    # source, destination
    pull = pickle.load(dbfile)                     
    dbfile.close()
    return pull, ind

def clean_up(test, year, toy_story, imdb_movies, poster_images):
    # get genre and content type from form
    genre = request.form.get('Genre')
    content_type = request.form.get('content_type')
    
    # if not selecting by content_type or genre set to default
    if content_type == 'Any':
        content_type = ''
    if genre == 'Any':
        genre = ''
        
    looking_for=10  # number of recommendations to look for
    
    # get the title id we are basing the recommendation off of
    m_test = imdb_movies[(imdb_movies.original_title==test)&(imdb_movies.year==year)].title_id.values[0]
    
    # get required portion of distance matrix as well as index for offset
    matrix, ind = get_pickle(m_test, imdb_movies)
    
    # calculate index for start of recommendations
    dex = (ind-np.argsort(matrix[0])[0])
    recommends = np.argsort(matrix[dex])[1:]
    
    # get titles and ids for top ten recommendations
    top_ten =imdb_movies.iloc[recommends][(imdb_movies.iloc[recommends].genre.str.contains(genre))&(imdb_movies.iloc[recommends].type.str.contains(content_type))].original_title[0:looking_for].values   

    ids = imdb_movies.iloc[recommends][(imdb_movies.iloc[recommends].genre.str.contains(genre))&(imdb_movies.iloc[recommends].type.str.contains(content_type))].title_id[0:looking_for].values

    # if poster is availble for title id then get image link else use missing poster link
    posters = []
    for vals in ids:
        if vals[0] == 't':
            val = int(vals[2:])
            if val in poster_images.imdbId.values:
                posters.append(poster_images[poster_images.imdbId==val].Poster.values[0])
                continue
        posters.append(toy_story)
    return top_ten, posters, test, ids 