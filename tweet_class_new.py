"""CSC110 Project: Tweet Class

Module Description
==================
This module contains the ...
"""

from typing import Set
import datetime

from dataclasses import dataclass

STATES = ['AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'GU', 'HI', 'IA',
          'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT',
          'NA', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI',
          'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY']


@dataclass
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
    date: str
