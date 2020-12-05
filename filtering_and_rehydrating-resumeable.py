"""
CSC110 PROJECT FILTERING_AND_REHYDRATING.PY
DATE: NOVEMBER 2020
GROUP: COURTNEY AMM, FAIZAH SAYYID, POORVI SHARMA, TINA ZHANG
"""
from twarc import Twarc
import tweet_class_new
import datetime
import json
import linecache
from typing import List

# internet solution to RecursionError: maximum recursion depth exceeded in __instancecheck__
# import sys
# sys.setrecursionlimit(100000000)  # 10000 is an example, try with different values

# FILL THESE OUT BEFORE ATTEMPTING TO USE THESE FUNCTIONS
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# DOCUMENT NAMES
raw_dataset = ''
processed_dataset = ''
final_dataset = ''


# Creating a twarc instance to rehydrate and sort the ids
t = Twarc(consumer_key,
          consumer_secret,
          access_token,
          access_token_secret)

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
               'Delaware': 'DE',
               'Florida': 'FL',
               'Georgia': 'GA',
               'Hawaii': 'HI',
               'Idaho': 'ID',
               'Illinois': 'IL',
               'Indiana': 'IN',
               'Iowa': 'IA',
               'Kansas': 'KS',
               'Kentucky': 'KY',
               'Louisiana': 'LA',
               'Maine': 'ME',
               'Maryland': 'MD',
               'Massachusetts': 'MA',
               'Michigan': 'MI',
               'Minnesota': 'MN',
               'Mississippi': 'MS',
               'Missouri': 'MO',
               'Montana': 'MT',
               'Nebraska': 'NE',
               'Nevada': 'NV',
               'New Hampshire': 'NH',
               'New Jersey': 'NJ',
               'New Mexico': 'NM',
               'New York': 'NY',
               'North Carolina': 'NC',
               'North Dakota': 'ND',
               'Ohio': 'OH',
               'Oklahoma': 'OK',
               'Oregon': 'OR',
               'Pennsylvania': 'PA',
               'Rhode Island': 'RI',
               'South Carolina': 'SC',
               'South Dakota': 'SD',
               'Tennessee': 'TN',
               'Texas': 'TX',
               'Utah': 'UT',
               'Vermont': 'VT',
               'Virginia': 'VA',
               'Washington': 'WA',
               'West Virginia': 'WV',
               'Wisconsin': 'WI',
               'Wyoming': 'WY'}

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


def num_of_lines(file_name: str):
    """Returns the number of lines in a file
    """
    return len([line.strip("\n") for line in open(file_name, 'r') if line != "\n"])


def resume() -> None:
    """compares the processed data to the raw data to see where the code stopped

    Preconditions:
        - open(processed_name, 'r') != None
    """
    raw = open(raw_dataset)
    process = open(processed_dataset, 'r')

    raw_file_length = len(set(raw.readlines()))
    process_set = {int(line[:18]) for line in process.readlines()}
    print(process_set)
    line = 0

    # while line % 11 != 0:
    #     raw_set.add(int(linecache.getline(raw_dataset, line)))
    #     line += 1
    # filter_tweets(list(raw_set.difference(process_set)))

    while line < raw_file_length:
        raw_set = set()
        line += 1

        while line % 10 != 0 and line < raw_file_length:
            raw_set.add(int(linecache.getline(raw_dataset, line)))
            line += 1
        raw_set.add(int(linecache.getline(raw_dataset, line)))

        if list(raw_set.difference(process_set)) != []:
            filter_tweets(list(raw_set.difference(process_set)))

    # process_set = set(int(line[:18]) for line in processed_file.readlines())
    # count = 1
    # for tweet in raw_set.difference(process_set):
    #     count += 1
    #     print(count)
    #     difference.write(str(tweet) + '\n')
    # difference.close()
    #
    # filter_tweets('difference_tracker.txt.02')


def filter_tweets(data: List[int]) -> None:
    """ This function reads a "dehydrated" list of tweet ids from the given file and dehydrates
    and filters these tweets based on location. If the tweet's location is in a specific US state,
    the tweet will be written to the given output file as a tweet object, with the Tweet's full
    text, hashtags, State location, and date created all stored in this object.

    Note: The commented out code in this function is incase someone needs the function to return a
    list of the tweet objects. If you need this functionailty, simply uncomment this code and edit
    the type contract.
    """
    processed = open(processed_dataset, 'a+')
    # destination
    f = open(final_dataset, "a+")
    # tweet_list = []

    for num in data:
        processed.write(str(num) + '\n')
    processed.close()

    for tweet in t.hydrate(data):
        temp_location = tweet["user"]["location"]
        retweet = tweet["full_text"][:2]

        if any(state in temp_location for state in states) and retweet != "RT":
            new_loc = get_location(temp_location)
            temp_date = get_date(tweet["created_at"])
            temp_hashtags = set()

            for element in tweet["entities"]["hashtags"]:
                temp_hashtags.add(element["text"])
            temp_tweet = tweet_class_new.Tweet(tweet["full_text"], temp_hashtags, new_loc, temp_date)

            # convert tweets to json
            json_tweet = json.dumps(temp_tweet.__dict__, sort_keys=True, default=str)

            f.write(str(json_tweet) + "\n")
            # tweet_list.append(tweet_class.Tweet(tweet["full_text"],
            #                                     temp_hashtags, new_loc, temp_date))
    f.close()
    # return tweet_list


def process_json_date(date: str):
    date_list = str.split(date, '-')
    if date_list[1][0] == '0':
        date_list[1] = date_list[1][1]

    if date_list[2][0] == '0':
        date_list[2] = date_list[2][1]

    return datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))


def process_json_hashtags(hashstring: str):
    if hashstring == 'set()':
        return set()
    else:
        tag_list = str.split(hashstring, "\'")
        tag_final_list = set()
        for index in range(0, len(tag_list)):
            if index % 2 == 1:
                tag_final_list.add(tag_list[index])

    return tag_final_list


def json_to_tweets():
    tweet_list = []
    with open(final_dataset) as f:
        for jsonObj in f:
            tweet_dict = json.loads(jsonObj)
            temp_date = process_json_date(tweet_dict['date'])
            temp_hashtags = process_json_hashtags(tweet_dict['hashtags'])
            tweet_list.append(tweet_class_new.Tweet(tweet_dict['text'], temp_hashtags,
                                                tweet_dict['state'], temp_date))
    return tweet_list
