import pandas as pd
import pickle
import numpy as np
from flask import Flask, Response, render_template, request, redirect

def get_pickle(imdbid, imdb_movies):
    ind = imdb_movies[imdb_movies.imdb_title_id==imdbid].index[0]
    lst = []
    for i in range(1,56):
        lst.append((i*1563)-1)
    for i in range(len(lst)):
        if ind < lst[i]:
            files = (lst[i])+1
            break
    dbfile = open(f'../chunks/weighted_imdb_test{int(files)}.pkl', 'rb')
    # source, destination
    pull = pickle.load(dbfile)                     
    dbfile.close()
    return pull, ind




"""
def get_pickle(imdbid):
    ind = imdb_movies[imdb_movies.imdb_title_id==imdbid].index[0]
    lst = []
    for i in range(1,56):
        lst.append((i*1563)-1)
    for i in range(len(lst)):
        if ind < lst[i]:
            files = (lst[i])+1
            break
    dbfile = open(f'../chunks/imdb_test{int(files)}.pkl', 'rb')
    # source, destination
    pull = pickle.load(dbfile)                     
    dbfile.close()
    return pull, ind
"""

def clean_up(movie_min, message, test, year, duration, toy_story, imdb_movies, poster_images):
    if duration == '':
        duration = 1000
    else:
        duration = int(duration)
    if duration < movie_min:
        message = "Sorry No Available Movies of that duration, try increasing Runtime"
    genre = request.form.get('Genre')
    if genre == '':
        genre = ' '
    looking_for=10
    print(genre)
    m_test = imdb_movies[(imdb_movies.original_title==test)&(imdb_movies.year==year)].imdb_title_id.item()
    matrix, ind = get_pickle(m_test, imdb_movies)
    dex = (ind-np.argsort(matrix[0])[0])
    recommends = np.argsort(matrix[dex])[1:]
    top_ten =imdb_movies.iloc[recommends][(imdb_movies.iloc[recommends].duration<=duration)&(imdb_movies.iloc[recommends].genre.str.contains(genre))].original_title[0:looking_for].values
#     top_ten = imdb_movies.iloc[recommends].original_title[0:10].values
    posters = []
    ids = imdb_movies.iloc[recommends][(imdb_movies.iloc[recommends].duration<=duration)&(imdb_movies.iloc[recommends].genre.str.contains(genre))].imdb_title_id[0:looking_for].values
    for vals in ids:
#     for vals in imdb_movies.iloc[recommends].imdb_title_id[0:10].values:
        val = int(vals[2:])
        if val in poster_images.imdbId.values:
            posters.append(poster_images[poster_images.imdbId==val].Poster.values[0])
        else:
            posters.append(toy_story)
    return message, top_ten, posters, test, ids 


"""if duration == '':
        duration = 1000
    else:
        duration = int(duration)
    if duration < movie_min:
        message = "Sorry No Available Movies of that duration, try increasing Runtime"
    genre = request.form.get('Genre')
    if genre == '':
        genre = ' '
    looking_for=10
    print(genre)
    if test == '':
        return redirect('/')
    year = test.replace(")","").split(" (")[1]
    test = test.replace(")","").split(" (")[0]
    if test not in imdb_movies.original_title.values:
        return redirect('/')
    m_test = imdb_movies[(imdb_movies.original_title==test)&(imdb_movies.year==year)].imdb_title_id.item()
    matrix, ind = get_pickle(m_test, imdb_movies)
    dex = (ind-np.argsort(matrix[0])[0])
    recommends = np.argsort(matrix[dex])[1:]
    top_ten =imdb_movies.iloc[recommends][(imdb_movies.iloc[recommends].duration<=duration)&(imdb_movies.iloc[recommends].genre.str.contains(genre))].original_title[0:looking_for].values
#     top_ten = imdb_movies.iloc[recommends].original_title[0:10].values
    posters = []
    for vals in imdb_movies.iloc[recommends][(imdb_movies.iloc[recommends].duration<=duration)&(imdb_movies.iloc[recommends].genre.str.contains(genre))].imdb_title_id[0:looking_for].values:
#     for vals in imdb_movies.iloc[recommends].imdb_title_id[0:10].values:
        val = int(vals[2:])
        if val in poster_images.imdbId.values:
            posters.append(poster_images[poster_images.imdbId==val].Poster.values[0])
        else:
            posters.append(toy_story)"""




"""<p>
<input type="submit" value="Recommed!">
<input type="reset" value="Reset Form">
</p>"""