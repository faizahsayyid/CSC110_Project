"""
CSC110 PROJECT FILTERING_AND_REHYDRATING.PY
DATE: NOVEMBER 2020
GROUP: COURTNEY AMM, FAIZAH SAYYID, POORVI SHARMA, TINA ZHANG


This module serves as the initial data processing function for the project.
The main function, filter_tweets, takes a file containing a "dehydrated" tweet
dataset (meaning that the dataset contains only tweet ids, and no other data
about the tweets), rehydrates those tweets, and then processes them to be our own
tweet datatypes. This is then written to a json lines file for future use. This process
also uses two helper functions, get_date and get_location

This module also contains the json_to_tweets function, which serves to process the
tweets written to the json lines file back in to a list of tweets to be used by our other
modules. This function uses one helper module, process_json_hashtags

Finally, there are two other functions, json_make_lowercase and shrink_dataset. These were
created to reprocess some of the dataset to better fit the needs of the other modules. The first
function makes the text and hashtags of the tweets in the jsonl file lowercase, the second shrinks
the dataset by a given amount in such a way that the data is still evenly distributed.

"""
import json
from twarc import Twarc
import tweet_class

# FILL THESE OUT BEFORE ATTEMPTING TO USE filter_tweets
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

# Creating a twarc instance to rehydrate and sort the ids
T = Twarc(CONSUMER_KEY,
          CONSUMER_SECRET,
          ACCESS_TOKEN,
          ACCESS_TOKEN_SECRET,
          tweet_mode="extended")

STATES_DICT = {'AL': 'AL', 'AK': 'AK', 'AZ': 'AZ', 'AR': 'AR', 'CA': 'CA', 'CO': 'CO', 'CT': 'CT',
               'DE': 'DE', 'FL': 'FL', 'GA': 'GA', 'HI': 'HI', 'ID': 'ID', 'IL': 'IL', 'IN': 'IN',
               'IA': 'IA', 'KS': 'KS', 'KY': 'KY', 'LA': 'LA', 'ME': 'ME', 'MD': 'MD', 'MA': 'MA',
               'MI': 'MI', 'MN': 'MN', 'MS': 'MS', 'MO': 'MO', 'MT': 'MT', 'NE': 'NE', 'NV': 'NV',
               'NH': 'NH', 'NJ': 'NJ', 'NM': 'NM', 'NY': 'NY', 'NC': 'NC', 'ND': 'ND', 'OH': 'OH',
               'OK': 'OK', 'OR': 'OR', 'PA': 'PA', 'RI': 'RI', 'SC': 'SC', 'SD': 'SD', 'TN': 'TN',
               'TX': 'TX', 'UT': 'UT', 'VT': 'VT', 'VA': 'VA', 'WA': 'WA', 'WV': 'WV', 'WI': 'WI',
               'WY': 'WY', 'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
               'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
               'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
               'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY',
               'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA',
               'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
               'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
               'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
               'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR',
               'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
               'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
               'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
               'Wisconsin': 'WI', 'Wyoming': 'WY'}

MONTHS = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07",
          "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}


# def get_date(tweetdate: str) -> str:
#     """Takes the String date of a tweet and processes it in to the string format used for the
#     tweet class
#
#     >>> get_date("Wed Oct 11 20:19:24 +0000 2018")
#     '2018-10-11'
#     """
#     date_list = str.split(tweetdate)
#     return date_list[-1] + '-' + MONTHS[date_list[1]] + '-' + date_list[2]
#
#
# def get_location(location: str) -> str:
#     """Takes the full location of a tweet and returns the state postal ID of that tweet
#
#     >>> get_location("San Francisco, California")
#     'CA'
#     >>> get_location("Albany, NY, United States")
#     'NY'
#
#     """
#     for state in STATES_DICT:
#         if state in location:
#             return STATES_DICT[state]
#
#     print("error: Location not found")
#     return 'error'
#
#
# def filter_tweets(input_file: str, output_file: str) -> None:
#     """ This function reads a "dehydrated" list of tweet ids from the given file and dehydrates
#     and filters these tweets based on location. If the tweet's location is in a specific US state,
#     the tweet will be written to the given output file as a tweet object, with the Tweet's full
#     text, hashtags, State location, and date created all stored in this object.
#     """
#     out = open(output_file, "w")
#
#     # Go through tweet ids line by line and rehydrate the tweet,
#     # giving us a twarc tweet object
#     for tweet in T.hydrate(open(input_file)):
#         # Take the location out of the tweet object (based on the user's location)
#         temp_location = tweet["user"]["location"]
#
#         # Used to check if the first two letters are "RT", which indicates the tweet
#         # is a retweet
#         retweet = tweet["full_text"][:2]
#
#         # Checks if current tweet is from the US, has a state specified, and is not
#         # a retweet. If it matches those criteria, then it is processed
#         if any(state in temp_location for state in STATES_DICT) and retweet != "RT":
#             # Gets the state postal code for the tweet based on its location
#             new_loc = get_location(temp_location)
#
#             # Processes the date to a datetime.time object
#             temp_date = get_date(tweet["created_at"])
#
#             # Since the hashtags of a tweet are stored as a dict in a list, this loop
#             # loops through the list and adds the text of each hashtag to a set
#             temp_hashtags = set()
#             for element in tweet["entities"]["hashtags"]:
#                 temp_hashtags.add(element["text"])
#
#             # Adds the tweet to a be in the format of our tweet data class objects
#             temp_tweet = tweet_class.Tweet(tweet["full_text"], temp_hashtags, new_loc, temp_date)
#
#             # Convert tweet objects to json objects in the format of a dictionary
#             json_tweet = json.dumps(temp_tweet.__dict__, sort_keys=True, default=str)
#
#             # Write each json object to a line in the jsonl file
#             out.write(str(json_tweet) + "\n")
#
#     # Closes the file we write to
#     out.close()


def process_json_hashtags(hashstring: str) -> set:
    """ Takes a string of hashtags in the format "{'hash_tag_name', 'hash_tag_name_2'}"
    and returns the hashtags as a set.

    >>> hashtags_list = process_json_hashtags("{'climatechange', 'spaceweather'}")
    >>> all(item in {'climatechange', 'spaceweather'} for item in hashtags_list)
    True
    >>> process_json_hashtags("set()")
    set()
    """
    # Checks if hashtag set is empty.
    if hashstring == 'set()':
        return set()
    # Otherwise processes hashtags to put them in a set
    else:
        # Split hashtags in to a list based on the ' character
        tag_list = str.split(hashstring, "\'")

        # Create the final hashtag list. The formatting ensures that a hashtag is stored
        # for only odd indices of the list, which the expression i % 2 == 1 checks for
        tag_final_list = {tag_list[i] for i in range(0, len(tag_list)) if i % 2 == 1}

    return tag_final_list


def json_to_tweets(input_file: str) -> list:
    """ Takes a json or jsonl file with json objects containing individual tweets and returns
    the list of tweet objects
    """
    tweet_list = []
    # Opens the input file
    with open(input_file) as inp:
        # Reads in each json object on each line of the input_file, and then processes it
        for json_obj in inp:
            # Loads the json file to a dictionary
            tweet_dict = json.loads(json_obj)

            # Processed the json hashtags from a string to a set
            temp_hashtags = process_json_hashtags(tweet_dict['hashtags'])

            # Appends the new tweet object on to the end of the tweet list
            tweet_list.append(tweet_class.Tweet(tweet_dict['text'], temp_hashtags,
                                                tweet_dict['state'], tweet_dict['date']))
    return tweet_list


def json_make_lowercase(input_file: str, output_file: str) -> None:
    """Takes a json or jsonl file with json objects containing individual tweets and makes
    both the text of the tweet and th hashtags all lower case. It then rewrites the tweets to
    a new jsonl with the new lowercase text.

    This function was added to make some of the keyword processing easier.
    """
    # Open the output file to write to
    out = open(output_file, "w")
    # Opens the input file
    with open(input_file) as inp:
        # Reads in each json object on each line of the input_file
        for json_obj in inp:
            # Loads the json file to a dictionary
            tweet_dict = json.loads(json_obj)

            # Update the text and hashtags of the tweet to be lowercase
            tweet_dict['text'] = tweet_dict['text'].lower()
            tweet_dict['hashtags'] = tweet_dict['hashtags'].lower()

            # Rewrite the tweet to a tweet object and then write that object to the output
            # jsonl file.
            temp_tweet = tweet_class.Tweet(tweet_dict['text'], tweet_dict['hashtags'],
                                           tweet_dict['state'], tweet_dict['date'])
            json_tweet = json.dumps(temp_tweet.__dict__, sort_keys=True, default=str)

            # Write to the outfile
            out.write(str(json_tweet) + "\n")
    # Close the outfile
    out.close()


def shrink_dataset(input_file: str, output_file: str, shrink_amt: int) -> None:
    """
    Takes an input jsonl file, shrinks by a factor given by shrink_amt while keeping the
    date distribution of data relatively the same, and rewrites this shrunk dataset to a
    new jsonl file.
    """
    # Open the output file to write to
    out = open(output_file, "w")

    # Set a counter for shrinking
    count = 0

    # Opens the input file
    with open(input_file) as inp:

        # Reads in each json object on each line of the input_file
        for json_obj in inp:

            # Only writes the json object to a new file if count is a multiple of shrink_amt
            # This is done to keep the distribution of data even as the dataset is shortened
            if count % shrink_amt == 0:

                # Loads the json file to a dictionary
                tweet_dict = json.loads(json_obj)

                temp_tweet = tweet_class.Tweet(tweet_dict['text'], tweet_dict['hashtags'],
                                               tweet_dict['state'], tweet_dict['date'])

                # Turn the tweet to a json object
                json_tweet = json.dumps(temp_tweet.__dict__, sort_keys=True, default=str)

                # Write to the outfile
                out.write(str(json_tweet) + "\n")

            count = count + 1

    out.close()


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['twarc', 'datetime', 'python_ta.contracts', 'tweet_class', 'json'],
        'max-line-length': 100,
        'allowed-io': ['shrink_dataset', 'filter_tweets', 'json_make_lowercase', 'json_to_tweets',
                       'get_location'],
        'disable': ['R1705', 'C0200']
    })
