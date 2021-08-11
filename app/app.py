from flask import Flask, Response, render_template, request, redirect
import json
from wtforms import TextField, Form
import pandas as pd
import pickle
import numpy as np
from all_help import get_pickle, clean_up


app = Flask(__name__)

imdb_movies = pd.read_csv("../Combined_Netflix_IMDb_Useful_Columns.csv", low_memory=False)
poster_images = pd.read_csv('../poster_image.csv')
toy_story = 'static/poster_not_found.png'
dbfile = open(f'../genre_list.pkl', 'rb')
genre_list = pickle.load(dbfile)                     
dbfile.close() 

class SearchForm(Form):
    autocomp = TextField('Title' ,id='movie_autocomplete')

@app.route('/_autocomplete', methods=['GET','POST'])
def autocomplete():
    dbfile = open(f'../all_title_list.pkl', 'rb')
    title = pickle.load(dbfile)                     
    dbfile.close()  
    return Response(json.dumps(title), mimetype='application/json')
    
    
@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm(request.form)
    return render_template("search.html", form=form, genre_list=genre_list)


@app.route('/action_page', methods=['GET','POST'])
def action_page():
    lst = []
    for val in imdb_movies.duration:
        if len(val)<4:
            lst.append(int(val))
    movie_min = min(lst)
#     movie_min = imdb_movies.duration.min()
    message='As well as:'
    test = request.form['autocomp']
    duration = request.form.get('Duration')
    if (test == '') or ('(' not in test):
        return redirect('/')
    year = test.replace(")","").split(" (")[1]
    test = test.replace(")","").split(" (")[0]
    if test not in imdb_movies.original_title.values:
        return redirect('/')
    message, top_ten, posters, test, ids = clean_up(movie_min, message, test, year, duration, toy_story, imdb_movies, poster_images)

    return render_template("user.html", movie_name=test, top_ten=top_ten, posters=posters, message=message, ids=ids)


if __name__=="__main__":
    app.run(debug=True)


    
#     imdb_movies.genre.str.contains(gen)
# imdb_movies.iloc[recommends][imdb_movies.iloc[recommends].duration<=duration].original_title[0:looking_for].values
    
#     imdb_movies.iloc[recommends][(imdb_movies.iloc[recommends].duration<=duration)&(imdb_movies.iloc[recommends].genre.str.contains(genre))].original_title[0:looking_for].values

    """
      <style>
          body {
      font-family: verdana;
      font-size: 20px;
      text-align: center;
      color: white;
      background-image: url("static/stock-vector-cinema-motion-picture-film-projector-with-different-film-reel-in-d-isometric-style-design-element-1268426137.jpg");
      background-repeat: no-repeat;
      background-attachment: fixed;
      background-size: cover;
    }
      </style>  
    """
    
#     <img src={{poster}} alt={{title}}>

# export FLASK_ENV=development