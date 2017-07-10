"""
    SheetManager will handle retrieving and writing to a
    google docs sheet
"""

from sheet_manager import SheetManager
from datetime import datetime
import time

class MovieManager(object):
    """
        Takes a sheet ID and checks for movies that have not been queried for
        a known available streaming service.
    """
    sheet_manager = None
    SHEET_NAME = 'Sheet1' #may or may not use this
    DATE_FORMAT = '%d/%m/%Y'#'merrrraca!

    def __init__(self, sheet_id):
        """
            Initialize the MovieManager with a sheet ID so the manager will know
            what sheet to read from and write to
        """
        self.sheet_manager = SheetManager(sheet_id)

    def get_movies(self, days=0, sheet_name='Sheet1'):
        """
            go through sheet and accumulate a list of movies that need to be
            updated. This include movies that haven't been updated in N days
            where N is an integer passed by the days argument or if the
            entry has not been checked before which is noted by the entry
            being undersized.
        """
        movie_list = []
        sheet = self.sheet_manager.get_sheet(sheet_name)

        current_date = datetime.strptime(time.strftime(self.DATE_FORMAT),
                self.DATE_FORMAT)

        for entry in sheet:
            if len(entry) > 1:
                """
                    entry should a list of 3 elements
                    if entry is greater than 1 then check
                    element 1 for a date and see if current
                    date - element 1's date is > days
                """
                entry_date = datetime.strptime(entry[1], self.DATE_FORMAT)
                if (current_date - entry_date).days >= days:
                    movie_list.append(entry[0])

            else:
                """
                    if only 1 element is present then add it
                    to the list there is no date to check
                """
                movie_list.append(entry[0])

        return movie_list

    def update_movies(self, movie_list, sheet_name):
        """
            Get old list, update relevent movies, send updated list to sheet
            manager
        """
        #print movie_list
        sheet = self.sheet_manager.get_sheet(sheet_name)

        movie_list_pos = 0
        for index in range(len(sheet)):
            #print('sheet title %s, list title %s'
            #        % (sheet[index][0], movie_list[movie_list_pos][0]))
            if sheet[index][0] == movie_list[movie_list_pos][0]:
                sheet[index] = movie_list[movie_list_pos]
                movie_list_pos += 1
                if movie_list_pos >= len(movie_list):
                    break
        #print sheet
        self.sheet_manager.update_sheet(sheet, sheet_name)
        return
