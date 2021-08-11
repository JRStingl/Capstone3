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
    message='As well as:'
    
    # get selection to base recommendation on and test validity
    test = request.form['autocomp']
    if (test == '') or ('(' not in test):
        return redirect('/')
    year = test.replace(")","").split(" (")[1]
    test = test.replace(")","").split(" (")[0]
    
    # if selection invalid then redirect to selection page
    if test not in imdb_movies.original_title.values:
        return redirect('/')
    
    # get required information to pass to recommendation page
    top_ten, posters, test, ids = clean_up(test, year, toy_story, imdb_movies, poster_images)

    return render_template("user.html", movie_name=test, top_ten=top_ten, posters=posters, message=message, ids=ids)


if __name__=="__main__":
    app.run(debug=True)

# export FLASK_ENV=development