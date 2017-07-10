"""
    This module will contain a manager for searching titles on JustWatch
    to find movies and what services they are currently on.
    An enum ProviderID is also available specifically for JustWatch since
    providers are identified as integers.
"""

from justwatch import JustWatch
from enum import Enum
import difflib
from sets import Set

class ProviderID(Enum):
    """
        This Enum contains the int for each provider's ID
    """
    NETFLIX = 8
    AMAZON_STR = 9
    HULU = 15

class JustWatchManager(object):
    """
    This class will act as a wrapped for the Just watch api to simplify
    the querying of movies from JustWatch to find providers for given
    titles.
    """
    MATCH_THRESH = 0.9
    just_watch = None

    def __init__(self):
        self.just_watch = JustWatch(country='US')

    def get_providers(self, movie_title='The Matrix'):
        """
            this method will be provided a movie title and will find
            the first title that is > 90% and return a list of its
            providers
        """
        lowered_title = movie_title.lower()
        query = self.just_watch.search_for_item(query=lowered_title)

        best_match = None

        for movie in query['items']:
            if difflib.SequenceMatcher(None,
                    lowered_title,
                    movie['title'].lower()).ratio() >= self.MATCH_THRESH:
                best_match = movie
                break

        if best_match is None:
            return None

        if best_match['offers'] is None:
            return None
        providers = Set()
        for provider in best_match['offers']:
            if int(provider['provider_id']) == ProviderID.NETFLIX.value:
                providers.add('Netflix')
                continue

            if int(provider['provider_id']) == ProviderID.AMAZON_STR.value:
                providers.add('Amazon')
                continue

            if int(provider['provider_id']) == ProviderID.HULU.value:
                providers.add('Hulu')
                continue

        if len(providers) == 0:
            return None

        return list(providers)
