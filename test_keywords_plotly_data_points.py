"""CSC110 Project: TESTING: Search For Keywords and Generating Data for Plotly

Module Description
==================
This module contains the functions for finding all keywords in a list of tweets, and sorting them
based on the number of time they occur.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of Faizah Sayyid, Tina Zhang,
Poorvi Sharma, and Courtney Amm (students at the University of Toronto St. George campus).
All forms of distribution of this code, whether as given or with any changes, are expressly
prohibited.

This file is Copyright (c) 2020 Faizah Sayyid, Tina Zhang, Poorvi Sharma, and Courtney Amm.
"""

import keywords_plotly_data_points
from tweet_class_new import Tweet


TWEET1 = Tweet(
    date='2018-01-10',
    hashtags={'ClimateChange', 'climatechangeisreal'},
    state='OH',
    text='Climate change is real'
)

TWEET2 = Tweet(
    date='2018-01-10',
    hashtags={'GlobalWarming', 'climatechange'},
    state='IL',
    text='The globe is warming'
)

TWEET3 = Tweet(
    date='2017-10-23',
    hashtags={'scientists', 'GlobalWarming'},
    state='CO',
    text='Scientists have proven that the globe is warming'
)

TWEET4 = Tweet(
    date='2018-08-06',
    hashtags={'climatechange', 'renewableenergy'},
    state='CA',
    text='When fossil fuels are burned, they release carbon dioxide and other greenhouse gases, which in turn trap '
         'heat in our atmosphere, making them the primary contributors to global warming and climate change.'
)

TWEET5 = Tweet(
    date='2018-11-27',
    hashtags=set(),
    state='PA',
    text='The climate is changing'
)


def test_tweets_to_words() -> None:
    """Test tweets_to_words with [TWEET1, TWEET4]"""


def test_tweet_phrase_freq() -> None:
    """Test tweet_phrase_freq with [TWEET2, TWEET3]"""


def test_find_key_phrases() -> None:
    """Test find_key_phrases with [TWEET2, TWEET3] and 2"""


def test_sorted_hashtag_freq() -> None:
    """Test sorted_hashtag_freq with """


def test_get_all_hashtags() -> None:
    """..."""


def test_find_key_hashtags() -> None:
    """..."""


def test_date_to_tweet() -> None:
    """..."""


def test_date_state_to_phrase_occurrences() -> None:
    """..."""


def test_data_points_key_phrase() -> None:
    """..."""


def test_key_phrases_to_data_points() -> None:
    """..."""


def test_date_state_to_hashtag_pop() -> None:
    """..."""


def test_data_points_hashtag() -> None:
    """..."""


def test_hashtags_to_data_points() -> None:
    """..."""


if __name__ == '__main__':
    import pytest
    pytest.main(['test_keywords_plotly_data_points.py', '-vv'])
