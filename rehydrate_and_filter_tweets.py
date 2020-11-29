"""
CSC110 PROJECT FILTERING_AND_REHYDRATING.PY
DATE: NOVEMBER 2020
GROUP: COURTNEY AMM, FAIZAH SAYYID, POORVI SHARMA, TINA ZHANG
"""
from twarc import Twarc
import tweet_class
import datetime
import json

# internet solution to RecursionError: maximum recursion depth exceeded in __instancecheck__
# import sys
# sys.setrecursionlimit(100000000)  # 10000 is an example, try with different values


# FILL THESE OUT BEFORE ATTEMPTING TO USE THESE FUNCTIONS
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# Creating a twarc instance to rehydrate and sort the ids
t = Twarc(consumer_key,
          consumer_secret,
          access_token,
          access_token_secret,
          tweet_mode="extended")

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", 'Alabama',
          'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
          'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana',
          'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts',
          'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
          'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota',
          'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
          'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
          'West Virginia', 'Wisconsin', 'Wyoming']

states_dict = {'AL': 'AL',
               'AK': 'AK',
               'AZ': 'AZ',
               'AR': 'AR',
               'CA': 'CA',
               'CO': 'CO',
               'CT': 'CT',
               'DC': 'DC',
               'DE': 'DE',
               'FL': 'FL',
               'GA': 'GA',
               'HI': 'HI',
               'ID': 'ID',
               'IL': 'IL',
               'IN': 'IN',
               'IA': 'IA',
               'KS': 'KS',
               'KY': 'KY',
               'LA': 'LA',
               'ME': 'ME',
               'MD': 'MD',
               'MA': 'MA',
               'MI': 'MI',
               'MN': 'MN',
               'MS': 'MS',
               'MO': 'MO',
               'MT': 'MT',
               'NE': 'NE',
               'NV': 'NV',
               'NH': 'NH',
               'NJ': 'NJ',
               'NM': 'NM',
               'NY': 'NY',
               'NC': 'NC',
               'ND': 'ND',
               'OH': 'OH',
               'OK': 'OK',
               'OR': 'OR',
               'PA': 'PA',
               'RI': 'RI',
               'SC': 'SC',
               'SD': 'SD',
               'TN': 'TN',
               'TX': 'TX',
               'UT': 'UT',
               'VT': 'VT',
               'VA': 'VA',
               'WA': 'WA',
               'WV': 'WV',
               'WI': 'WI',
               'WY': 'WY',
               'Alabama': 'AL',
               'Alaska': 'AK',
               'Arizona': 'AZ',
               'Arkansas': 'AR',
               'California': 'CA',
               'Colorado': 'CO',
               'Connecticut': 'CT',
               'Delaware': 'DC',
               'Florida': 'DE',
               'Georgia': 'FL',
               'Hawaii': 'GA',
               'Idaho': 'HI',
               'Illinois': 'ID',
               'Indiana': 'IL',
               'Iowa': 'IN',
               'Kansas': 'IA',
               'Kentucky': 'KS',
               'Louisiana': 'KY',
               'Maine': 'LA',
               'Maryland': 'ME',
               'Massachusetts': 'MD',
               'Michigan': 'MA',
               'Minnesota': 'MI',
               'Mississippi': 'MN',
               'Missouri': 'MS',
               'Montana': 'MO',
               'Nebraska': 'MT',
               'Nevada': 'NE',
               'New Hampshire': 'NV',
               'New Jersey': 'NH',
               'New Mexico': 'NJ',
               'New York': 'NM',
               'North Carolina': 'NY',
               'North Dakota': 'NC',
               'Ohio': 'ND',
               'Oklahoma': 'OH',
               'Oregon': 'OK',
               'Pennsylvania': 'OR',
               'Rhode Island': 'PA',
               'South Carolina': 'RI',
               'South Dakota': 'SC',
               'Tennessee': 'SD',
               'Texas': 'TN',
               'Utah': 'TX',
               'Vermont': 'UT',
               'Virginia': 'VT',
               'Washington': 'VA',
               'West Virginia': 'WA',
               'Wisconsin': 'WV',
               'Wyoming': 'WI'}

months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9,
          "Oct": 10, "Nov": 11, "Dec": 12}


def get_date(tweetdate: str):
    """Returns the datetime values of tweets
    """
    date_list = str.split(tweetdate)
    return datetime.date(int(date_list[-1]), months[date_list[1]], int(date_list[2]))


def get_location(location: str):
    """Returns the location of tweets
    """
    for state in states_dict:
        if state in location:
            return states_dict[state]

    print("error: Location not found")
    return -2


def filter_tweets() -> None:
    """ This function reads a "dehydrated" list of tweet ids from the given file and dehydrates
    and filters these tweets based on location. If the tweet's location is in a specific US state,
    the tweet will be written to the given output file as a tweet object, with the Tweet's full
    text, hashtags, State location, and date created all stored in this object.

    Note: The commented out code in this function is incase someone needs the function to return a
    list of the tweet objects. If you need this functionailty, simply uncomment this code and edit
    the type contract.
    """
    f = open("rehydrate_02.json", "w")
    # tweet_list = []

    for tweet in t.hydrate(open('climate_id.txt.02')):
        temp_location = tweet["user"]["location"]

        if any(state in temp_location for state in states):
            new_loc = get_location(temp_location)
            temp_date = get_date(tweet["created_at"])
            temp_hashtags = set()

            for element in tweet["entities"]["hashtags"]:
                temp_hashtags.add(element["text"])
            temp_tweet = tweet_class.Tweet(tweet["full_text"], temp_hashtags, new_loc, temp_date)

            # convert tweets to json
            json_tweet = json.dumps(temp_tweet.__dict__, sort_keys=True, default=str)
            f.write(str(json_tweet))
            # tweet_list.append(tweet_class.Tweet(tweet["full_text"],
            #                                     temp_hashtags, new_loc, temp_date))
    f.close()
    # return tweet_list
