"""CSC110 Project: Sorting Tweets

Module Description
==================
This module contains functions for filtering lists of tweets by hashtags and dates,
then further by location and popularity
"""
from tweet_class import Tweet
from typing import List, Dict, Set
import datetime


def filter_by_hashtag_and_date(hashtag: str, year: int, tweets: List[Tweet]) -> List[Tweet]:
    """Return set of tweets that contain the given hashtag and were tweeted during the
    given year
    >>> t1 = Tweet({'#climatechange', '#hurricane', '#wildfires', '#globalwarming'}, 'CA', datetime.date(2018, 9, 14))
    >>> t2 = Tweet({'#actonclimate', '#climatechangeisreal', '#globalwarming'}, 'AL', datetime.date(2019, 9, 14))
    >>> t3 = Tweet({'#climatechangeisfalse', '#climatechangehoax'}, 'OH', datetime.date(2015, 9, 14))
    >>> t4 = Tweet({'#climatechange', '#globalwarming'}, 'CA', datetime.date(2016, 9, 14))
    >>> result = filter_by_hashtag_and_date('#climatechange', 2018, [t1, t2, t3])
    >>> result == [t1]
    True
    """

    filtered_so_far = []

    for tweet in tweets:
        if hashtag in tweet.hashtags and tweet.date.year == year:
            filtered_so_far.append(tweet)

    return filtered_so_far


def location_to_popularity(tweets: List[Tweet]) -> Dict[str, List[Tweet]]:
    """Return a dictionary of the given tweets where the keys are the state it was tweeted from,
    and the values are the number of tweets per location
    """


if __name__ == '__main__':
    import doctest
    doctest.testmod()
