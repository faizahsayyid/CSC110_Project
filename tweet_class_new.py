"""CSC110 Project: Tweet Class

Module Description
==================
This module contains the ...
"""

from typing import Set
from dataclasses import dataclass

STATES = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA',
          'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
          'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT',
          'VA', 'WA', 'WV', 'WI', 'WY']


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
        - self.text.islower()
        - all(hashtag.islower() for hashtag in self.hashtags)

    >>> tweet = Tweet('some text', {'#climatechange', '#climatechangehoax', '#globalwarming'}, 'CA', \
    '2018-02-12')
    """
    text: str
    hashtags: Set[str]
    state: str
    date: str


if __name__ == '__main__':

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['typing', 'dataclasses'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
