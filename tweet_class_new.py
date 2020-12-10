"""CSC110 Project: Tweet Class

Module Description
==================
This module contains the ...
"""

from typing import Set
import datetime

from dataclasses import dataclass
# internet solution https://stackoverflow.com/questions/8230315/how-to-json-serialize-sets
from json import dumps, loads, JSONEncoder, JSONDecoder
import pickle

states = ['AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'GU', 'HI', 'IA',
          'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT',
          'NA', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI',
          'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY']


class Tweet:
    """ A date type representing a tweet

    Instance Attributes:
        - hashtags: the hashtags used in the tweet
        - state: the state the tweet was tweeted from
        - date: the date the tweet was tweeted

    Representation Invariants:
        - self.text != ''
        - self.state in states

    >>> tweet = Tweet('some text', {'#climatechange', '#climatechangehoax', '#globalwarming'}, 'CA', \
                    datetime.date(2015, 9, 14))
    """
    text: str
    hashtags: Set[str]
    state: str
    date: datetime.date

    def __init__(self, text: str, hashtags: Set[str], state: str, date: datetime.date):
        self.text = text
        self.hashtags = hashtags
        self.state = state
        self.date = date


# internet solution https://stackoverflow.com/questions/8230315/how-to-json-serialize-sets
# saving these in case we need them in the future
# class PythonObjectEncoder(JSONEncoder):
#     def default(self, obj):
#         # if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
#         #     return JSONEncoder.default(self, obj)
#         return {'_python_object': pickle.dumps(obj)}
#
#
# class SetEncoder(JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, set):
#             return list(obj)
#         return JSONEncoder.default(self, obj)
#
# def as_python_object(dct):
#     if '_python_object' in dct:
#         return pickle.loads(str(dct['_python_object']))
#     return dct
