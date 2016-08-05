import nltk
import string
from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()


def get_most_common_phrases(txtfile):
    # change this to read in your data
    with open(txtfile) as wordfile:
        text = wordfile.read()

    exclude = set(string.punctuation)
    text = ''.join(ch for ch in text if ch not in exclude)

    tokens = nltk.wordpunct_tokenize(text)
    finderbigram = BigramCollocationFinder.from_words(tokens)
    findertrigram = TrigramCollocationFinder.from_words(tokens)

    # only phrases that appear 3+ times
    finderbigram.apply_freq_filter(3)
    findertrigram.apply_freq_filter(3)

    # return the 10 n-grams with the highest score
    twowordphrases = finderbigram.nbest(bigram_measures.pmi, 10)
    threewordphrases = findertrigram.nbest(bigram_measures.pmi, 10)

    return twowordphrases, threewordphrases
