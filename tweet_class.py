"""CSC110 Project: Tweet Class

Module Description
==================
This module contains the ...
"""

from typing import Set
import datetime
from dataclasses import dataclass

states = ['AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN',
          'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT', 'NA', 'NC', 'ND', 'NE', 'NH', 'NJ',
          'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA',
          'WI', 'WV', 'WY']


@dataclass
class Tweet:
    """ A date type representing a tweet

    Instance Attributes:
        - hashtags: the hashtags used in the tweet
        - state: the state the tweet was tweeted from
        - date: the date the tweet was tweeted

    Representation Invariants:
        - self.state in states
    """

    hashtags: Set[str]
    state: str
    date: datetime.date

    # def __init__(self, hashtags: Set[str], state: str, date: datetime.date):
    #     self.hashtags = hashtags
    #     self.state = state
    #     self.date = date
