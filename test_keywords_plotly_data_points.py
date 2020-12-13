"""CSC110 Project: TESTING: Search For Keywords and Generating Data for Plotly

Module Description
==================
This module contains testing for the functions in the module keywords_plotly_data_points

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of Faizah Sayyid, Tina Zhang,
Poorvi Sharma, and Courtney Amm (students at the University of Toronto St. George campus).
All forms of distribution of this code, whether as given or with any changes, are expressly
prohibited.

This file is Copyright (c) 2020 Faizah Sayyid, Tina Zhang, Poorvi Sharma, and Courtney Amm.
"""

import keywords_plotly_data_points
from tweet_class import Tweet


TWEET1 = Tweet(
    date='2018-01-10',
    hashtags={'climatechange', 'climatechangeisreal'},
    state='OH',
    text='climate change is real'
)

TWEET2 = Tweet(
    date='2018-01-10',
    hashtags={'globalwarming', 'climatechange'},
    state='IL',
    text='the globe is warming'
)

TWEET3 = Tweet(
    date='2017-10-23',
    hashtags={'scientists', 'globalwarming'},
    state='CO',
    text='scientists have proven that the globe is warming'
)

TWEET4 = Tweet(
    date='2018-08-06',
    hashtags={'climatechange', 'renewableenergy'},
    state='CA',
    text='when fossil fuels are burned, they release carbon dioxide and other greenhouse gases, '
         'which in turn trap heat in our atmosphere, making them the primary contributors to '
         'global warming and climate change.'
)

TWEET5 = Tweet(
    date='2018-11-27',
    hashtags=set(),
    state='PA',
    text='the climate is changing'
)

LIST_OF_TWEETS = [TWEET1, TWEET2, TWEET3, TWEET4, TWEET5]


def test_tweets_to_words() -> None:
    """Test tweets_to_words with [TWEET1, TWEET4]"""
    actual = keywords_plotly_data_points.tweets_to_words([TWEET1, TWEET4])

    expected = ['climate', 'change', 'real', 'fossil', 'fuels', 'burned', 'release', 'carbon',
                'dioxide', 'greenhouse', 'gases', 'turn', 'trap', 'heat', 'atmosphere', 'making',
                'primary', 'contributors', 'global', 'warming', 'climate', 'change']

    assert actual == expected


def test_tweet_phrase_freq() -> None:
    """Test tweet_phrase_freq with [TWEET2, TWEET3]"""

    actual = keywords_plotly_data_points.tweet_phrase_freq([TWEET2, TWEET3])

    expected = [(1, ('globe',)), (1, ('scientists',)), (2, ('globe', 'warming')),
                (1, ('warming', 'scientists')), (1, ('scientists', 'proven')),
                (1, ('proven', 'globe')), (1, ('globe', 'warming', 'scientists')),
                (1, ('warming', 'scientists', 'proven')), (1, ('scientists', 'proven', 'globe')),
                (1, ('proven', 'globe', 'warming'))]

    assert actual == expected


def test_find_key_phrases() -> None:
    """Test find_key_phrases with [TWEET2, TWEET3] and 2"""
    actual = keywords_plotly_data_points.find_key_phrases([TWEET2, TWEET3], 2)

    # Since the function sorts in reverse and the many of the phrases have
    # the same frequency, it will take the tuple with the largest inner tuple and lowest letter
    # in alphabetical order to be the 2nd key phrase

    expected = [('globe', 'warming'), ('warming', 'scientists', 'proven')]

    assert actual == expected


def test_sorted_hashtag_freq() -> None:
    """Test sorted_hashtag_freq with LIST_OF_TWEETS"""

    actual = keywords_plotly_data_points.sorted_hashtag_freq(LIST_OF_TWEETS)

    expected = [(3, 'climatechange'), (2, 'globalwarming'), (1, 'scientists'),
                (1, 'renewableenergy'), (1, 'climatechangeisreal')]

    assert actual == expected


def test_get_all_hashtags() -> None:
    """Test get_all_hashtags with LIST_OF_TWEETS"""

    actual = keywords_plotly_data_points.get_all_hashtags(LIST_OF_TWEETS)

    expected = ['climatechange', 'climatechangeisreal', 'globalwarming', 'climatechange',
                'globalwarming', 'scientists', 'renewableenergy', 'climatechange']

    assert set(actual) == set(expected)


def test_find_key_hashtags() -> None:
    """Test find_key_hashtags with LIST_OF_TWEETS and 2"""

    actual = keywords_plotly_data_points.find_key_hashtags(LIST_OF_TWEETS, 2)

    expected = ['climatechange', 'globalwarming']

    assert actual == expected


def test_date_to_tweet() -> None:
    """Test date_to_tweet on LIST_OF_TWEETS"""

    result = keywords_plotly_data_points.date_to_tweet(LIST_OF_TWEETS)

    assert result['2018-01-10'][0] == TWEET1
    assert result['2018-01-10'][1] == TWEET2

    assert result['2017-10-23'][0] == TWEET3

    assert result['2018-08-06'][0] == TWEET4

    assert result['2018-11-27'][0] == TWEET5


if __name__ == '__main__':
    import pytest
    pytest.main(['test_keywords_plotly_data_points.py', '-vv'])

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['tweet_class_new', 'keywords_plotly_data_points'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
