import pandas as pd
import pickle
import numpy as np
from flask import Flask, Response, render_template, request, redirect
from urllib.parse import urlencode, urlparse, parse_qs
from lxml.html import fromstring
from requests import get


def get_pickle(imdbid, imdb_movies):
    ind = imdb_movies[imdb_movies.title_id==imdbid].index[0]
    lst = []
    for i in range(1,100):
        lst.append((i*1433)-1)
        # lst.append((i*1563)-1)
    for i in range(len(lst)):
        if ind < lst[i]:
            files = (lst[i])+1
            break
    dbfile = open(f'../distance/translated_weights_full_set{int(files)}.pkl', 'rb')
    # dbfile = open(f'../distance/full_set{int(files)}.pkl', 'rb')
    # dbfile = open(f'../chunks/imdb_test{int(files)}.pkl', 'rb')
    # source, destination
    pull = pickle.load(dbfile)                     
    dbfile.close()
    return pull, ind

def get_netflix_link(title):
    title = "+".join(title.split())
    raw = get(f"https://www.google.com/search?q=netflix+{title}").text
    page = fromstring(raw)
    lst = raw.split("https://www.netflix.com/title/")
    link = "https://www.netflix.com/title/" + lst[1].split('&')[0]
    return link

def get_imdb_link(title, c_type, c_year):
    title = "+".join(title.split())
    title = title +"+"+ c_type +"+"+ c_year
    print(title)
    raw = get(f"https://www.google.com/search?q=imdb+{title}").text
    page = fromstring(raw)
    lst = raw.split("https://www.imdb.com/title/")
    print(len(lst))
    link = "https://www.imdb.com/title/" + lst[1].split('/')[0]
    return link, lst[1].split('/')[0]

def clean_up(movie_min, message, test, year, duration, toy_story, imdb_movies, poster_images):
    if duration == '':
        duration = 1000
    else:
        duration = int(duration)
    if duration < movie_min:
        message = "Sorry No Available Movies of that duration, try increasing Runtime"
    genre = request.form.get('Genre')
    content_type = request.form.get('content_type')
    if genre == '':
        genre = ' '
    looking_for=10
#     print(genre)
    m_test = imdb_movies[(imdb_movies.original_title==test)&(imdb_movies.year==year)].title_id.values[0]
    print(m_test)
    matrix, ind = get_pickle(m_test, imdb_movies)
    dex = (ind-np.argsort(matrix[0])[0])
    recommends = np.argsort(matrix[dex])[1:]
    top_ten =imdb_movies.iloc[recommends][(imdb_movies.iloc[recommends].genre.str.contains(genre))].original_title[0:looking_for].values
    top_ids =imdb_movies.iloc[recommends][(imdb_movies.iloc[recommends].genre.str.contains(genre))].title_id[0:looking_for].values
#     top_ten = imdb_movies.iloc[recommends].original_title[0:10].values
    posters = []
    ids = imdb_movies.iloc[recommends][(imdb_movies.iloc[recommends].genre.str.contains(genre))].title_id[0:looking_for].values
    new_ids=[]
    for m_id, title in zip(ids,top_ten):
        if m_id[0]=='s':
            # _, imdb_id = get_imdb_link(imdb_movies[imdb_movies.title_id==id].original_title)
            c_type=imdb_movies[imdb_movies.title_id==m_id].type
            c_year=imdb_movies[imdb_movies.title_id==m_id].year
            print(m_id, title, year)
            _, imdb_id = get_imdb_link(title, c_type, c_year)
            new_ids.append(imdb_id)
        else:
            new_ids.append(m_id)
    ids = new_ids      
    for vals in ids:
#     for vals in imdb_movies.iloc[recommends].imdb_title_id[0:10].values:
        val = int(vals[2:])
        if val in poster_images.imdbId.values:
            posters.append(poster_images[poster_images.imdbId==val].Poster.values[0])
        else:
            posters.append(toy_story)
    return message, top_ten, posters, test, ids 
