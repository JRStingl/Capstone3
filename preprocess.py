import pickle
import pandas as pd
import numpy as np
from deep_translator import GoogleTranslator

def make_poster_file():
    # create id and poster link only CSV for Flask
    posters = pd.read_csv('data/MovieGenre.csv')
    post = posters[['imdbId','Poster']].copy()
    post.dropna(inplace=True)
    post.to_csv("poster_image.csv")
    return

def make_genre_file():
    #create genre list for Flask
    genres_maybe = total_list.genre.unique()
    collect = []

    # split genre list and add genre types to set
    for genre in genres_maybe:
        collect.append(genre.split(", "))
    set_test = set()
    for val in collect:
        if isinstance(val,list):
            for tes in val:
                set_test.add(tes)
        else:
            set_test.add(val)
    # go through set and split compound genres into components and add all components to set        
    collect = []
    for genre in set_test:
        collect.append(genre.split(" & "))
    set_test = set()
    for val in collect:
        if isinstance(val,list):
            for tes in val:
                set_test.add(tes)
        else:
            set_test.add(val)
    # save CSV of genre list in case offline editing is desired
    pd.DataFrame(data=set_test, columns=['Genres']).to_csv('genre_to_edit.csv')
    return 'genre_to_edit.csv'

if __name__ == "__main__":
    # load data from CSVs into pandas dataframes
    netflix = pd.read_csv("data/netflix_titles.csv")
    imdb_movies = pd.read_csv("data/IMDb movies.csv", low_memory=False)

    # rename features for clarity
    netflix.rename(columns = {'show_id': 'title_id', 'title': 'original_title','release_year': 'year', 'listed_in': 'genre','cast': 'actors' },inplace=True)
    imdb_movies.rename(columns = {'imdb_title_id': 'title_id'},inplace=True)

    # select features intended for use
    imdb_cutdown = imdb_movies[['title_id','type','original_title','director','actors','year','duration','genre','description']].copy()
    netflix_cutdown = netflix[['title_id','type','original_title','director','actors','year','duration','genre','description']].copy()

    # combine the dataframes
    total_list = imdb_cutdown.copy()
    for i in range(netflix_cutdown.shape[0]):
        total_list=total_list.append(netflix_cutdown.iloc[i])

    # reset index and drop old index
    total_list = total_list.reset_index()
    total_list.drop('index',inplace=True, axis=1)

    # output combined dateframe as a CSV for future use
    total_list.to_csv("Combined_Netflix_IMDb_Useful_Columns.csv")

    # translate description
    translated = GoogleTranslator(source='auto', target='en')
    total_list.description = total_list.description.apply(lambda x: translated.translate(x))
    total_list.to_csv("translated_in_case.csv")

    # create id and poster link only CSV for Flask
    make_poster_file()

    # create CSV file for offline editing in case desired 
    genre_file_name = make_genre_file(total_list)

    # after any offline cleanup desired read CSV back in and create pickle file
    genre_list = pd.read_csv(genre_file_name).Genres.to_list()
    dbfile = open('genre_list.pkl', 'ab')
    pickle.dump(genre_list, dbfile)                     
    dbfile.close()


