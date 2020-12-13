"""CSC110 Project: Search For Keywords and Generating Data for Plotly

Module Description
==================
The module keywords_plotly_data_points:
    - Finds the keywords/phrases and key hashtags within in a lists of tweets (using the nltk
    library)
    - The number of times these keywords/phrases and key hashtags occur in each state on
    a particular date
    - Organizes the above data into data points formatted for plotly

Find keywords/phrases and key hashtags:

The first step to finding keywords was to separated the tweet text in to a list of words, removing
words that are obviously not keywords, such as 'the' 'and', 'is', etc, as well as punctuation. This
was done in our function tweets_to_word using nltk.word_tokenize, nltk.sent_tokenize, nltk.corpus.stopwords,
as well as the hard coded constants PUNCTUATION, and OTHER. Next, in our function get_relative_frequencies,
key phrases/collocations were founds using nltk.collocations.BigramCollocationFinder and
nltk.collocations.TrigramCollocationFinder. Bi-grams are two word combinations, while trigrams are three word
combinations. Finally all of single words (excluding words that aren't nouns using nltk.pos_tag), bi-grams, and
trigrams are ranked by frequency to find the keywords (with in the same function). All of this was put together
in the function find_key_phrases.

A similar approach was taken for find_key_hashtags. The first two steps, turning text into a list of words,
and finding the bi-grams and trigrams were skipped. Instead we simply gathered all the hashtags and found their
frequencies.

Date, State to Keyword Occurrences & Plotly Data Points:

Having found the keywords and key hashtags, we then found their prevalence in each state on particular dates.
To do this we found all the dates that tweets were tweeted from our data (in our function date_to_tweet), and used
the hard coded constant STATES to get all the combinations of dates and states. Then, we iterated through each
combination to find the prevalence of a given keyword in date_state_to_phrase_occurrences and
date_state_to_hashtag_pop. This gave us a dictionary in the form {(date, state), occurrences}.

From there, we converted the data from this format to one supported by plotly, which is three lists, one for each of
dates, states, and occurrences where for index i (list1[i], list2[i], list3[i]) corresponds to a single data point.
This was done in our function data_points.


Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of Faizah Sayyid, Tina Zhang,
Poorvi Sharma, and Courtney Amm (students at the University of Toronto St. George campus).
All forms of distribution of this code, whether as given or with any changes, are expressly
prohibited.

This file is Copyright (c) 2020 Faizah Sayyid, Tina Zhang, Poorvi Sharma, and Courtney Amm.
"""
import nltk
from nltk import collocations
from nltk.corpus import stopwords
from tweet_class_new import Tweet
from typing import List, Dict, Tuple, Any
from rehydrate_and_filter_tweets import json_to_tweets
from pprint import pprint

PUNCTUATION = ['.', ',', '!', '?', ';', ':', "'", '‘', '’', '“', '``', "''", '-', '”', '&', '/',
               '#', '|', '--', ')', '(', '*', '....', '=']

OTHER = ['@', 'https', "'s", 'u', '...', '..', '%', '$', '—', '–', '\u2066', "'ve", "'re", "'m",
         "n't", 'the…']

STATES = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS',
          'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC',
          'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']


# ==================================================================================================
# Functions for getting the data points for our plotly graph (for hashtags)
# ==================================================================================================

def hashtags_to_data_points(tweets: List[Tweet], num_key_hashtags: int) -> \
        Dict[str, Tuple[List[str], List[str], List[int]]]:
    """Return a dictionary where the keys are the key hashtags from the tweets and the values are
    the data points corresponding to that hashtag.
    """
    key_hashtags = find_key_hashtags(tweets, num_key_hashtags)

    data_points_dict_so_far = {}

    for hashtag in key_hashtags:
        data_points_dict_so_far['#' + hashtag] = data_points_hashtag(tweets, hashtag)

    return data_points_dict_so_far


def data_points_hashtag(tweets: List[Tweet], hashtag: str) \
        -> Tuple[List[str], List[str], List[int]]:
    """Return a list of lists where each corresponding index in the lists counts as one data point
    for a plotly map animation that displays number of occurrences of the search_phrase for each
    state over time.

        - First list (element 0): list of the dates
        - Second list (element 1): list of the states
        - Third list (element 2): list of the popularity of the hashtag for the
                                    corresponding date and state
    """
    d_s_to_hashtag_pop = date_state_to_hashtag_pop(tweets, hashtag)

    return data_points(d_s_to_hashtag_pop)


def date_state_to_hashtag_pop(tweets: List[Tweet], hashtag: str) -> Dict[Tuple[str, str], int]:
    """Return a dictionary where the keys are a tuples of dates and states (dates are strings),
    and the corresponding values is the popularity of the given hashtag in that state at that time
    """
    date_to_t = date_to_tweet(tweets)

    # ACCUMULATOR d_s_to_occs_so_far dictionary of {(state, date): popularity}
    # initial value: all the combinations of dates and states to zero
    d_s_to_hashtag_pop = {(date, state): 0 for date in date_to_t for state in STATES}

    for date_state in d_s_to_hashtag_pop:
        date, state = date_state

        for tweet in date_to_t[date]:

            if hashtag in tweet.hashtags and (tweet.state == state):
                if date_state in d_s_to_hashtag_pop:
                    d_s_to_hashtag_pop[date_state] += 1

    return d_s_to_hashtag_pop


# ==================================================================================================
# Functions for getting the data points for our plotly graph (for key phrases)
# ==================================================================================================

def key_phrases_to_data_points(tweets: List[Tweet], num_key_phrases: int) -> \
        Dict[str, Tuple[List[str], List[str], List[int]]]:
    """Return a dictionary where the keys are the key phrases from the tweets and the values are
    the data points corresponding to that key phrase.
    """
    # ACCUMULATOR data_points_dict_so_far builds the dict of hashtags to the corresponding
    # data points
    data_points_dict_so_far = {}

    key_phrases = find_key_phrases(tweets, num_key_phrases)

    for phrase in key_phrases:
        str_phrase = ' '.join(phrase)
        data_points_dict_so_far[str_phrase] = data_points_key_phrase(tweets, phrase)

    return data_points_dict_so_far


def data_points_key_phrase(tweets: List[Tweet], search_phrase) \
        -> Tuple[List[str], List[str], List[int]]:
    """Return a list of lists where each corresponding index in the lists counts as one data point
    for a plotly map animation that displays number of occurrences of the search_phrase for each
    state over time.

        - First list (element 0): list of the dates
        - Second list (element 1): list of the states
        - Third list (element 2): list of the # of occurrences
    """
    d_s_to_occs = date_state_to_phrase_occurrences(tweets, search_phrase)

    return data_points(d_s_to_occs)


def date_state_to_phrase_occurrences(tweets: List[Tweet], search_phrase: tuple) \
        -> Dict[Tuple[str, str], int]:
    """Return a dictionary where the keys are a tuples of dates and states (dates are strings),
    and the corresponding values are the number of times the search_phrase occurs in every tweet
    that was tweeted on that date and in that state
    """

    date_to_t = date_to_tweet(tweets)

    # ACCUMULATOR d_s_to_occs_so_far dictionary of {(state, date): occurrences}
    # initial value: all the combinations of dates and states to zero
    d_s_to_occs_so_far = {(date, state): 0 for date in date_to_t for state in STATES}

    for date_state in d_s_to_occs_so_far:

        date, state = date_state

        for tweet in date_to_t[date]:
            if date_state in d_s_to_occs_so_far and (tweet.state == state):
                d_s_to_occs_so_far[date_state] += phrase_occurrences_in_tweet(tweet, search_phrase)

    return d_s_to_occs_so_far

    # d_s_to_occs_so_far = {}
    #
    # for tweet in tweets:
    #     date_state = (tweet.date, tweet.state)
    #     if date_state in d_s_to_occs_so_far:
    #         d_s_to_occs_so_far[date_state] += phrase_occurrences_in_tweet(tweet, search_phrase)
    #     elif date_state not in d_s_to_occs_so_far:
    #         d_s_to_occs_so_far[date_state] = phrase_occurrences_in_tweet(tweet, search_phrase)
    #
    # return d_s_to_occs_so_far


# ==================================================================================================
# Helper functions for making the plotly animation data points
# ==================================================================================================

def date_to_tweet(tweets: List[Tweet]) -> Dict[str, List[Tweet]]:
    """Return a dictionary where the keys are all the dates that a tweet occurred within the
    given list of tweets, and the values are the tweets that occured on that day"""

    # ACCUMULATOR d_to_t_so_far builds a dictionary from dates to list of tweets
    d_to_t_so_far = {}

    for tweet in tweets:
        if tweet.date in d_to_t_so_far:
            d_to_t_so_far[tweet.date].append(tweet)
        else:
            d_to_t_so_far[tweet.date] = [tweet]

    return d_to_t_so_far


def data_points(data_dict: Dict[Tuple[str, str], int]) -> Tuple[List[str], List[str], List[int]]:
    """Return a tuple of lists for the given data that corresponds to format plotly needs for a
    map graph animation

    >>> d = {('a', 'dogs'): 1, ('b', 'cats'): 3, ('c', 'bunnies'): 4}
    >>> data_points(d)
    (['a', 'b', 'c'], ['dogs', 'cats', 'bunnies'], [1, 3, 4])
    """
    sorted_keys = sorted(list(data_dict.keys()))

    # ACCUMULATOR listed_data_1 keeps track of the first element of every key
    listed_data_1 = []

    # ACCUMULATOR listed_data_2 keeps track of the second element of every key
    listed_data_2 = []

    # ACCUMULATOR listed_data_3 keeps track of the corresponding values of every key
    listed_data_3 = []

    for key in sorted_keys:
        listed_data_1.append(key[0])
        listed_data_2.append(key[1])
        listed_data_3.append(data_dict[key])

    return (listed_data_1, listed_data_2, listed_data_3)


# ==================================================================================================
# Function for finding the number of times a a phrase occurs in a tweet
# ==================================================================================================

def phrase_occurrences_in_tweet(tweet: Tweet, search_phrase: tuple) -> int:
    """Return number of times a a phrase occurs in a tweet

    Phrases includes:
    - uni-grams - single words
    - bi-grams (aka two words that are commonly used together)
    - tri-grams (aka three words that are commonly used together)

    >>> t = Tweet(text='what is life. life is meaningless. meaningless is life.', hashtags=set(), \
      state='ME', date='2018-02-12')
    >>> phrase_occurrences_in_tweet(t, ('life',))
    3
    >>> phrase_occurrences_in_tweet(t, ('life', 'meaningless'))
    1
    """

    # ACCUMULATOR occurrences_so_far keeps track of the # of times search_phrase occurs
    # in the tweet
    occurrences_so_far = 0

    word_list = tweet_to_words(tweet)

    bigrams = list(nltk.bigrams(word_list))

    trigrams = list(nltk.trigrams(word_list))

    tuple_word_list = [tuple([word]) for word in word_list]

    phrases = tuple_word_list + bigrams + trigrams

    for phrase in phrases:
        if phrase == search_phrase:
            occurrences_so_far += 1

    return occurrences_so_far


# ==================================================================================================
# Function for finding key hashtags
# ==================================================================================================

def find_key_hashtags(tweets: List[Tweet], num_key_hashtags: int) -> List[str]:
    """Return a list of the key hashtags with length num_wanted"""

    wanted_key_hashtags = sorted_hashtag_freq(tweets)[:num_key_hashtags]

    return [x[1] for x in wanted_key_hashtags]


def get_all_hashtags(tweets: List[Tweet]) -> List[str]:
    """Return a list of all the hashtags fro the given list of tweets"""

    # ACCUMULATOR hashtags_so_far keeps track of all the hashtags in tweets
    hashtags_so_far = []

    for tweet in tweets:
        hashtags_so_far.extend(tweet.hashtags)

    return hashtags_so_far


def sorted_hashtag_freq(tweets: List[Tweet]) -> List[Tuple[int, str]]:
    """ Return the frequency of each hashtag within the given list of hashtags"""

    hashtags = get_all_hashtags(tweets)

    freqs_dict = keys_to_freq(hashtags)

    return sorted(dict_to_tuple_list(freqs_dict), reverse=True)


# ==================================================================================================
# Function for finding key phrases from a list of tweets
# ==================================================================================================

def find_key_phrases(tweets: List[Tweet], num_key_phrases: int) -> List[tuple]:
    """Return a list of key phrases from the given list of tweets with length num_key_phrases

    Precondition:
        - num_key_phrases <= len(phrases_to_occurrences(tweets)) # the # of phrases in the tweets
    """
    phrase_freqs = sorted(tweet_phrase_freq(tweets), reverse=True)

    key_phrases = phrase_freqs[:num_key_phrases]

    return [p[1] for p in key_phrases]


# ==================================================================================================
# Function for finding phrases in tweets and how often they occur
# ==================================================================================================

def tweet_phrase_freq(tweets: List[Tweet]) -> List[Tuple[int, tuple]]:
    """ Return list of frequency and phrase pairs for all the text in the given tweets

     Phrases includes:
        - uni-grams - single words
        - bi-grams (aka two words that are commonly used together)
        - tri-grams (aka three words that are commonly used together)
    """

    words_from_tweets = tweets_to_words(tweets)

    return get_relative_frequencies(words_from_tweets)


# ==================================================================================================
# Helper Functions for tweet_phrase_freq
# ==================================================================================================

def tweets_to_words(tweets: List[Tweet]) -> List[str]:
    """Return a words in the text of tweets where each word is separated into a list of string

    Excludes words such as 'and', 'the', 'as', 'he', 'her', etc (provided by nltk.corpus.stopwords)
    in returned list. Also does not include punctuation.
    """
    # ACCUMULATOR words_so_far keeps track of the words in the tweet
    words_so_far = []

    for tweet in tweets:
        words_so_far.extend(tweet_to_words(tweet))

    return words_so_far


def tweet_to_words(tweet: Tweet) -> List[str]:
    """Return a words in the text of a tweet where each word is separated into a list of string

    Excludes words such as 'and', 'the', 'as', 'he', 'her', etc (provided by nltk.corpus.stopwords)
    in returned list. Also does not include punctuation.

    >>> t = Tweet(text='what is life. life is meaningless. meaningless is life.', hashtags=set(), \
      state='ME', date='2018-02-12')
    >>> tweet_to_words(t)
    ['life', 'life', 'meaningless', 'meaningless', 'life']
    """
    # ACCUMULATOR words_so_far keeps track of the words in the tweet
    words_so_far = []

    # List of words to not include in our final returned list
    unwanted_words = stopwords.words('english')
    unwanted_words.extend(PUNCTUATION + OTHER)

    # Break up tweet into sentences
    sentences_list = nltk.sent_tokenize(tweet.text)

    # Break up sentences into words
    for sent in sentences_list:
        words = nltk.word_tokenize(sent)
        for word in words:
            words_so_far.append(word)

    # Remove unwanted words
    copy_of_words = words_so_far.copy()

    for word in copy_of_words:
        if word in unwanted_words:
            words_so_far.remove(word)
        elif '//t.co/' in word or '@' in word or any(c.isdigit() for c in word):
            words_so_far.remove(word)

    return words_so_far


def get_nouns(words: List[str]) -> List[str]:
    """Return a list of all the nouns from the given words

    >>> get_nouns(['say', 'climate', 'oil', 'fire', 'when', 'what'])
    ['climate', 'oil', 'fire']
    """
    tagged_words = nltk.pos_tag(words)

    return [tagged_word[0] for tagged_word in tagged_words
            if (tagged_word[1] == 'NN') or (tagged_word[1] == 'NNS')]


def keys_to_freq(keys: List[Any]) -> Dict[Any, int]:
    """Return a dictionary where the keys are all the unique values in keys, the values and the
    frequencies of each key in keys the number of time each key in keys appears to phrase counts

    >>> result = keys_to_freq(['a', 'b', 'c', 'a', 'a', 'b', 'a'])
    >>> result == {'a': 4, 'b': 2, 'c': 1}
    True
    """

    # ACCUMULATOR key_freqs_so_far builds the dictionary from key to frequency
    key_freqs_so_far = {}

    for key in keys:
        if key in key_freqs_so_far:
            key_freqs_so_far[key] += 1
        elif key not in key_freqs_so_far:
            key_freqs_so_far[key] = 1

    return key_freqs_so_far


def get_n_grams(finder: collocations.AbstractCollocationFinder) -> List[Tuple[tuple, int]]:
    """Return all the bigrams from the given finder, scored by frequency

    >>> my_finder = collocations.BigramCollocationFinder.from_words(['what', 'is', 'life'])
    >>> get_n_grams(my_finder)
    [(1, ('what', 'is')), (1, ('is', 'life'))]
    """

    scored_n_grams = list(finder.ngram_fd.items())

    inverted_scored_ngrams = [(b[1], b[0]) for b in scored_n_grams]

    return inverted_scored_ngrams


def get_relative_frequencies(words: List[str]) -> List[Tuple[int, tuple]]:
    """ Return a list of the relative frequencies and phrases from words

    Relative frequencies are the amount of time each phrase appears in words divided by len(words)

     Phrases includes:
    - uni-grams - single words
    - bi-grams (aka two words that are commonly used together)
    - tri-grams (aka three words that are commonly used together)

    >>> result = get_relative_frequencies(['what', 'is', 'life', 'life', 'is', 'meaningless'])
    >>> expected = [(2, ('life',)), (1, ('what', 'is')), (1, ('is', 'life')), (1, ('life', 'life')),\
     (1, ('life', 'is')), (1, ('is', 'meaningless')), (1, ('what', 'is', 'life')), \
     (1, ('is', 'life', 'life')), (1, ('life', 'life', 'is')), (1, ('life', 'is', 'meaningless'))]
    >>> result == expected
    True
    """
    # ACCUMULATOR phrase_count_so_far build dictionary from phrases to occurrences
    scored_phrases_so_far = []

    # Get all the bigrams, trigrams, and bigrams from words
    bigram_finder = collocations.BigramCollocationFinder.from_words(words)
    trigram_finder = collocations.TrigramCollocationFinder.from_words(words)

    # Get the frequencies of all the unigrams (only the nouns) and add it to scored_phrases_so_far
    unigram_freq_dict = keys_to_freq(get_nouns(words))

    unigram_freq_dict = {tuple([unigram]): unigram_freq_dict[unigram]
                         for unigram in unigram_freq_dict}

    scored_phrases_so_far.extend(dict_to_tuple_list(unigram_freq_dict))

    # Get the frequencies of all the bigrams and trigrams, and add them to scored_phrases_so_far
    scored_phrases_so_far.extend(get_n_grams(bigram_finder))
    scored_phrases_so_far.extend(get_n_grams(trigram_finder))

    return scored_phrases_so_far


def dict_to_tuple_list(d: Dict[Any, int]) -> List[Tuple[int, Any]]:
    """Return a list of tuples sorted based on the value of each key value pair in d

    >>> result = dict_to_tuple_list({'a': 1, 'b': 2, 'c': 3})
    >>> set(result) == {(1, 'a'), (2, 'b'), (3, 'c')}
    True
    """
    # ACCUMULATOR tuple_list_so_far keep track of all the int and value pair
    tuple_list_so_far = []

    for key in d:
        tuple_list_so_far.append((d[key], key))

    return tuple_list_so_far


def list_tuple_to_list_str(list_of_tuple: List[tuple]) -> List[str]:
    """ Return a list of strings given a list of tuples

    >>> list_tuple_to_list_str([('climate', 'change'), ('What', 'is', 'life')])
    ['climate change', 'What is life']
    """
    return [' '.join(t) for t in list_of_tuple]


# ==================================================================================================
# Example
# ==================================================================================================

def run_example() -> None:
    """ Example of find_key_phrases on the file:
                Year/Fall 2020/csc110/assignments/CSC110_Project/Datasets/Samples
    """
    tweets = json_to_tweets()
    key_phrases_tuples = find_key_phrases(tweets, 30)

    key_phrases = list_tuple_to_list_str(key_phrases_tuples)

    print('Key Phrases:')

    pprint(key_phrases)

    print()
    print('Key Hashtags:')
    pprint(find_key_hashtags(tweets, 10))

    print()
    print('Data Points (key phrase  - "climate change"):')
    data = data_points_key_phrase(tweets, ('climate', 'change'))
    pprint(data)

    print()
    print(sum(data[2]))

    print()
    print('Key Phrases to Data Points:')
    key_phrases_to_data = key_phrases_to_data_points(tweets, 5)
    pprint(key_phrases_to_data)

    print()
    print('Key Hashtags to Data Points')
    hashtags_to_data = hashtags_to_data_points(tweets, 5)
    pprint(hashtags_to_data)


if __name__ == '__main__':
    run_example()

    import doctest
    doctest.testmod()
