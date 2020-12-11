"""CSC110 Project: Search For Keywords

Module Description
==================
This module contains the functions for finding all keywords in a list of tweets, and sorting them based on
the number of time they occur.
"""
import nltk
from nltk import collocations
from nltk.corpus import stopwords
from tweet_class_new import Tweet
from typing import List, Dict, Tuple, Any
from rehydrate_and_filter_tweets import json_to_tweets
from pprint import pprint

PUNCTUATION = ['.', ',', '!', '?', ';', ':', "'", '‘', '’', '“', '``', "''", '-', '”', '&', '/', '#', '|', '--', ')',
               '(', '*', '....', '=']
OTHER = ['@', 'https', "'s", 'u', '...', '..', '%', '$', '—', '–', '\u2066', "'ve", "'re", "'m",
         "n't", 'the…']


def lists_of_dates_states_occurrences(tweets: List[Tweet], search_phrase) -> Tuple[List[str], List[str], List[int]]:
    """Return a list of lists where each corresponding index

        - First list (element 0): list of the dates
        - Second list (element 1): list of the states
        - Third list (element 2): list of the # of occurrences
    """
    d_s_to_occs = date_state_to_occurrences(tweets, search_phrase)
    sorted_keys = sorted(list(d_s_to_occs.keys()))

    list_of_states = []
    list_of_dates = []
    list_of_occurrences = []

    for key in sorted_keys:
        list_of_states.append(key[0])
        list_of_dates.append(key[1])
        list_of_occurrences.append(d_s_to_occs[key])

    return (list_of_dates, list_of_states, list_of_occurrences)


def date_state_to_occurrences(tweets: List[Tweet], search_phrase: tuple) -> Dict[Tuple[str, str], int]:
    """Return a dictionary where the keys are a tuples of dates and states (dates are strings), and the
    corresponding values are the number of times the search_phrase occurs in every tweet that was tweeted
    on that date and in that state
    """
    d_s_to_occs_so_far = {}

    for tweet in tweets:
        date_state = (tweet.date, tweet.state)
        if date_state in d_s_to_occs_so_far:
            d_s_to_occs_so_far[date_state] += phrase_occurences_in_tweet(tweet, search_phrase)
        elif date_state not in d_s_to_occs_so_far:
            d_s_to_occs_so_far[date_state] = phrase_occurences_in_tweet(tweet, search_phrase)

    return d_s_to_occs_so_far


def phrase_occurences_in_tweet(tweet: Tweet, search_phrase: tuple) -> int:
    """Return whether phrase is in the text

    Phrases includes:
    - uni-grams - single words
    - bi-grams (aka two words that are commonly used together)
    - tri-grams (aka three words that are commonly used together)
    - quad-grams (aka four words that are commonly used together)
    """

    sentences_list = nltk.sent_tokenize(tweet.text.lower())

    word_list = []
    occurences = 0

    unwanted_words = stopwords.words('english')
    unwanted_words.extend(PUNCTUATION)
    unwanted_words.extend(OTHER)

    for sent in sentences_list:
        word_list.extend(nltk.word_tokenize(sent))

    # Remove unwanted words
    copy_of_words = word_list.copy()

    for word in copy_of_words:
        if word in unwanted_words:
            word_list.remove(word)
        elif '//t.co/' in word or '@' in word or any(c.isdigit() for c in word):
            word_list.remove(word)

    bigrams = list(nltk.bigrams(word_list))

    trigrams = list(nltk.trigrams(word_list))

    tuple_word_list = [tuple([word]) for word in word_list]

    phrases = []
    phrases.extend(tuple_word_list + bigrams + trigrams)

    for phrase in phrases:
        if phrase == search_phrase:
            occurences += 1

    return occurences


# ==================================================================================================
# Function for finding key hashtags
# ==================================================================================================

def find_key_hashtags(tweets: List[Tweet], num_wanted: int) -> List[str]:
    """Return a list of the key hashtags with length num_wanted"""

    wanted_key_hashtags = sorted_hashtag_freq(tweets)[:num_wanted]

    return [x[1] for x in wanted_key_hashtags]


def get_all_hashtags(tweets: List[Tweet]) -> List[str]:
    """Return a list of all the hashtags fro the given list of tweets"""
    hashtags_so_far = []

    for tweet in tweets:
        hashtags_so_far.extend([hashtag.lower() for hashtag in tweet.hashtags])

    return hashtags_so_far


def sorted_hashtag_freq(tweets: List[Tweet]) -> List[Tuple[int, str]]:
    """ Return the frequency of each hashtag within the given list of hashtags"""

    hashtags = get_all_hashtags(tweets)

    freqs_dict = keys_to_freq(hashtags)

    return sorted(dict_to_tuple_list(freqs_dict), reverse=True)


# ==================================================================================================
# Function for finding phrases in tweets and how often they occur
# ==================================================================================================

def tweet_phrase_freq(tweets: List[Tweet]) -> List[Tuple[float, tuple]]:
    """ Return a corpus including all the relevant phrases from the text of a list of tweets.
    Each of the phrases will be scored based on there frequency in the list of tweets.

     Phrases includes:
        - uni-grams - single words
        - bi-grams (aka two words that are commonly used together)
        - tri-grams (aka three words that are commonly used together)
    """

    words_from_tweets = tweets_to_words(tweets)

    return get_relative_frequencies(words_from_tweets)


# ==================================================================================================
# Function for finding key phrases from a list of tweets
# ==================================================================================================


def find_key_phrases(tweets: List[Tweet], num_keyphrases: int) -> List[tuple]:
    """Return a list of key phrases from the given list of tweets with length num_keyphrases

    Precondition:
        - num_keyphrases <= len(phrases_to_occurrences(tweets)) # the # of phrases in the tweets
    """
    phrase_freqs = sorted(tweet_phrase_freq(tweets), reverse=True)

    keyphrases = phrase_freqs[:num_keyphrases]

    return [p[1] for p in keyphrases]


# ==================================================================================================
# Helper Functions for tweet_phrase_freq
# ==================================================================================================

def tweets_to_words(tweets: List[Tweet]) -> List[str]:
    """Return a words in the text of a tweets where each word is separated into a list of string

    Excludes words such as 'and', 'the', 'as', 'he', 'her', etc (provided by nltk.corpus.stopwords) in
    returned list. Also does not include punctuation.
    """
    # ACCUMULATOR words_so_far keeps track of the words in the tweet
    words_so_far = []

    # List of words to not include in our final returned list
    unwanted_words = stopwords.words('english')
    unwanted_words.extend(PUNCTUATION)
    unwanted_words.extend(OTHER)

    sentences_so_far = []

    for tweet in tweets:
        # Break up tweet into sentences
        sentences_list = nltk.sent_tokenize(tweet.text.lower())
        sentences_so_far.extend(sentences_list)

    # Break up sentences into words
    for sent in sentences_so_far:
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
    """Return a list of all the nouns from the given words"""
    tagged_words = nltk.pos_tag(words)

    return [tagged_word[0] for tagged_word in tagged_words if tagged_word[1] == 'NN' or tagged_word[1] == 'NNS']


def keys_to_freq(keys: List[Any]) -> Dict[Any, int]:
    """Return a dictionary where the keys are all the unique values in keys, the values and the frequencies of
    each key in keys the number of time each key in keys appears to phrase counts"""

    key_freqs_so_far = {}

    for key in keys:
        if key in key_freqs_so_far:
            key_freqs_so_far[key] += 1
        elif key not in key_freqs_so_far:
            key_freqs_so_far[key] = 1

    return key_freqs_so_far


def get_n_grams(finder: collocations.AbstractCollocationFinder) -> List[Tuple[tuple, int]]:
    """Return all the bigrams from the words"""

    scored_n_grams = list(finder.ngram_fd.items())

    inverted_scored_ngrams = [(b[1], b[0]) for b in scored_n_grams]

    return inverted_scored_ngrams


def get_relative_frequencies(words: List[str]) -> List[Tuple[float, tuple]]:
    """ Return a list of the relative frequencies and phrases from words

    Relative frequencies are the amount of time each phrase appears in words divided by len(words)

     Phrases includes:
    - uni-grams - single words
    - bi-grams (aka two words that are commonly used together)
    - tri-grams (aka three words that are commonly used together)
    - quad-grams (aka four words that are commonly used together)
    """
    # ACCUMULATOR phrase_count_so_far build dictionary from phrases to occurrences
    scored_phrases_so_far = []

    # Get all the bigrams, trigrams, and bigrams from words
    bigram_finder = collocations.BigramCollocationFinder.from_words(words)
    trigram_finder = collocations.TrigramCollocationFinder.from_words(words)

    # Get the frequencies of all the unigrams (only the nouns) and add it to scored_phrases_so_far
    unigram_freq_dict = keys_to_freq(get_nouns(words))
    unigram_freq_dict = {tuple([unigram]): unigram_freq_dict[unigram] for unigram in unigram_freq_dict}
    scored_phrases_so_far.extend(dict_to_tuple_list(unigram_freq_dict))

    # Get the frequencies of all the bigrams and trigrams, and add them to scored_phrases_so_far
    scored_phrases_so_far.extend(get_n_grams(bigram_finder))
    scored_phrases_so_far.extend(get_n_grams(trigram_finder))

    return scored_phrases_so_far


def dict_to_tuple_list(d: Dict[Any, int]) -> List[Tuple[int, Any]]:
    """Return a list of tuples sorted based on the value of each key value pair in d
     """
    tuple_list_so_far = []

    for key in d:
        tuple_list_so_far.append((d[key], key))

    return tuple_list_so_far


def list_tuple_to_list_str(list_of_tuple: List[tuple]) -> List[str]:
    """ Return a list of strings given a list of tuples"""
    return [' '.join(t) for t in list_of_tuple]


# ==================================================================================================
# Example
# ==================================================================================================

def run_example_find_deniers() -> None:
    """ Example of find_key_phrases on the file:  Year/Fall 2020/csc110/assignments/CSC110_Project/Datasets/Samples
    """
    tweets = json_to_tweets()
    deniers = [tweet for tweet in tweets if ('climatechangehoax' in tweet.hashtags)]
    phrases = find_key_phrases(deniers, 80)

    pprint(phrases)


def run_example() -> None:
    """ Example of find_key_phrases on the file:  Year/Fall 2020/csc110/assignments/CSC110_Project/Datasets/Samples
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
    print('Phrase in Tweet?')
    print(tweets[0].text)
    print()
    print(key_phrases_tuples[0])
    print_thing = phrase_occurences_in_tweet(tweets[0], key_phrases_tuples[0])
    print(print_thing)


if __name__ == '__main__':
    run_example()
