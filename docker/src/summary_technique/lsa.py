from nltk.tokenize import sent_tokenize, word_tokenize
from numpy.linalg import svd as singular_value_decomposition
from paper import Paper
import numpy
import summary
from flask import current_app
import config
import math
from collections import namedtuple
from operator import attrgetter

SENT_NUM = 1
PREPROCESS_SENT_NUM = 5
SUMMARY_FOLDER = config.get_summary_path()
MIN_DIMENSIONS = 3
REDUCTION_RATIO = 1/1
SentenceInfo = namedtuple("SentenceInfo", ("sentence", "order", "rating",))

def preprocess_input(text:str, sent_num:str=PREPROCESS_SENT_NUM) -> str:
    result = summarize_text(text, sent_num)
    print("[lsa preprocess] ", result)
    return result

def summarize_text(text:str, sent_num:int=SENT_NUM) -> str:
    print(sent_num)
    if(len(text) == 0):
        return ""

    dictionary = _create_dictionary(text)
    sentences = sent_tokenize(text)

    matrix = _create_matrix(text, dictionary)
    matrix = _compute_term_frequency(matrix)

    u, sigma, v = singular_value_decomposition(matrix, full_matrices=False)

    ranks = iter(_compute_ranks(sigma, v))
    result = _get_best_sentences(
        sentences,
        sent_num,
        lambda s: next(ranks)
    )
    # print(result)
    result_str = ''
    for sentence in result:
        # print("[lsa] sentence:", sentence)
        result_str += sentence
    print("[lsa] result: " , len(word_tokenize(result_str)), "\n")
    return result_str


def _normalize_word(word:str):
    return word.lower()

def _create_dictionary(text:str) -> dict[str, int]:
    """Creates mapping key = word, value = row index"""
    words = word_tokenize(text)
    words = tuple(words)
        
    words = map(_normalize_word, words)

    # unique_words contain words that are not in stop word list
    unique_words = frozenset(w for w in words if w not in summary.get_stop_word_list())

    # w for word, i for index
    dict_result = dict((w, i) for i, w in enumerate(unique_words))
    return dict_result

def _create_matrix(text:str, dictionary:dict[str, int]):
    """
    Creates matrix of shape where cells
    contains number of occurences of words (rows) in senteces (cols).
    """
    sentences = sent_tokenize(text)
    # print("[lsa] sentences:", sentences)
    words_count = len(dictionary)
    sentences_count = len(sentences)
    if words_count < sentences_count:
        message = (
            "Number of words (%d) is lower than number of sentences (%d). "
            "LSA algorithm may not work properly."
        )
        current_app.logger.warning(message % (words_count, sentences_count))

    matrix = numpy.zeros((words_count, sentences_count))
    for col, sentence in enumerate(sentences):
        words = word_tokenize(sentence)
        for word in words:
            # only valid words is counted (not stop-words, ...)
            if word in dictionary:
                row = dictionary[word]
                matrix[row, col] += 1

    return matrix

def _compute_term_frequency(matrix, smooth=0.4):
    """
    Computes TF metrics for each sentence (column) in the given matrix and  normalize 
    the tf weights of all terms occurring in a document by the maximum tf in that document 
    according to ntf_{t,d} = a + (1-a)\frac{tf_{t,d}}{tf_{max}(d)^{'}}.
        
    The smoothing term $a$ damps the contribution of the second term - which may be viewed 
    as a scaling down of tf by the largest tf value in $d$
    """
    assert 0.0 <= smooth < 1.0

    max_word_frequencies = numpy.max(matrix, axis=0)
    rows, cols = matrix.shape
    for row in range(rows):
        for col in range(cols):
            max_word_frequency = max_word_frequencies[col]
            if max_word_frequency != 0:
                frequency = matrix[row, col]/max_word_frequency
                matrix[row, col] = smooth + (1.0 - smooth)*frequency

    return matrix

def _compute_ranks(sigma, v_matrix):
    assert len(sigma) == v_matrix.shape[0]

    dimensions = max(MIN_DIMENSIONS,
        int(len(sigma)*REDUCTION_RATIO))
    powered_sigma = tuple(s**2 if i < dimensions else 0.0
        for i, s in enumerate(sigma))

    ranks = []
        
    for column_vector in v_matrix.T:
        rank = sum(s*v**2 for s, v in zip(powered_sigma, column_vector))
        ranks.append(math.sqrt(rank))

    return ranks

def _get_best_sentences(sentences, count, rating, *args, **kwargs):
    # print('[lsa] count:', count, "\n")
    rate = rating
    if isinstance(rating, dict):
        assert not args and not kwargs
        rate = lambda s: rating[s]

    infos = (SentenceInfo(s, o, rate(s, *args, **kwargs))
        for o, s in enumerate(sentences))

    # sort sentences by rating in descending order
    infos = sorted(infos, key=attrgetter("rating"), reverse=True)

    # print("[lsa] infos before:", infos, "\n")
    infos = infos[:count]
    # print("[lsa] infos after:", infos, "\n")
    # sort sentences by their order in document
    infos = sorted(infos, key=attrgetter("order"))

    return tuple(i.sentence for i in infos)

if __name__ == "__main__":
    print("HI")
