#!/usr/bin/python
"""
    This module will initialize a MovieManager and get a list of movies
    that need to be updated, get there info from a JustWatch manager
    and send the list back to the MovieManager to update the sheet.
"""

from movie_manager import MovieManager
from justwatch_manager import JustWatchManager
import time

SHEET_ID = '1QV33cljsmuv61cy2dPgWS3Xqdx0AsJjaS8XTi-z8Y1U'
SHEET_NAME = 'Sheet1'

DATE_FORMAT = '%d/%m/%Y'
#NOTE movie manager requires that the date be formatted like so

def update_list():
    """
        perform an update on the sheet
    """
    movie_manager = MovieManager(SHEET_ID)
    justwatch_manager = JustWatchManager()
    current_date = time.strftime(DATE_FORMAT)

    movie_list = movie_manager.get_movies(7, SHEET_ID)
    if len(movie_list) == 0:
        return
    updated_movie_list = []
    for movie in movie_list:
        movie_name = movie
        providers = justwatch_manager.get_providers(movie_name)
        if providers is None:
            providers = "None"
        else:
            providers = ', '.join(providers)
        updated_movie_list.append([movie_name, current_date, providers])
    #print updated_sheet
    movie_manager.update_movies(updated_movie_list, SHEET_NAME)

update_list()
