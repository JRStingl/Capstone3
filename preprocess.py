import pandas as pd
import numpy as np



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