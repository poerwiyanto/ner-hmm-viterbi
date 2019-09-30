"""
    File name: viterbi.py
    Author: Poerwiyanto
    Date created: 4/26/2019
    Date last modified: 4/26/2019
    Python version: 3.7.1
"""
from nltk import ngrams


class Viterbi(object):
    def __init__(self, entities, tokens):
        self.entities = entities
        self.tokens = tokens

        self.__unigrams = {}
        self.__bigrams = {}
        self.trigram_probs = {}
        self.emission_probs = {}
        self.words = {}

        for row, row_value in enumerate(entities):
            # Add unigrams into dictionary.
            for column, unigram in enumerate(row_value):
                self.emission_probs[(tokens[row][column], unigram)] =\
                    1 + self.emission_probs.get((tokens[row][column], unigram), 0)
                self.__unigrams[unigram] = 1 + self.__unigrams.get(unigram, 0)

            # Generate and add bigrams into dictionary.
            bigrams = ngrams(['*', '*'] + row_value + ['stop'], 2)
            for bigram in bigrams:
                self.__bigrams[bigram] = 1 + self.__bigrams.get(bigram, 0)

            # Generate and add trigrams into dictionary.
            trigrams = ngrams(['*', '*'] + row_value + ['stop'], 3)
            for trigram in trigrams:
                self.trigram_probs[trigram] =\
                    1 + self.trigram_probs.get(trigram, 0)

        # Step 1: Add words into dictionary.
        for row in tokens:
            for token in row:
                self.words[token] = 1 + self.words.get(token, 0)

        # Step 2: Get trigram probabilities.
        for key in self.trigram_probs:
            self.trigram_probs[key] /= self.__bigrams[(key[0], key[1])]

        # Step 3: Get emission probabilities.
        for key in self.emission_probs:
            self.emission_probs[key] /= self.__unigrams[key[1]]

    def __K(self, index):
        if index == -1 or index == -2:
            return ['*']
        elif index >= 0:
            return list(self.__unigrams.keys())

    def tag(self, tokens):
        """Trigram HMM using Viterbi algorithm based on http://www.cs.columbia.edu/~mcollins/hmms-spring2013.pdf."""
        result = []
        for row, tokens_ in enumerate(tokens):
            bp = {}
            pi = {(-1, '*', '*'): 1}
            sentence = []
            for column, token in enumerate(tokens_):
                if self.words.get(token, 0) == 0:
                    sentence.append('UNK')
                else:
                    sentence.append(token)

            for k in range(len(sentence)):
                for u in self.__K(k - 1):
                    for v in self.__K(k):
                        max_pi = float('-inf')
                        for w in self.__K(k - 2):
                            temp =\
                                pi[(k - 1, w, u)] *\
                                self.trigram_probs.get((w, u, v), 0) *\
                                self.emission_probs.get((sentence[k], v), 0)
                            if max_pi < temp:
                                max_pi = temp
                                pi[(k, u, v)] = max_pi
                                bp[(k, u, v)] = w

            max_last = float('-inf')
            tags = {}
            for u in self.__K(len(sentence) - 2):
                for v in self.__K(len(sentence) - 1):
                    temp =\
                        pi[(len(sentence) - 1, u, v)] *\
                        self.trigram_probs.get((u, v, 'stop'), 0)
                    if max_last < temp:
                        max_last = temp
                        tags[len(sentence) - 1] = v
                        tags[len(sentence) - 2] = u

            for k in range(len(sentence) - 3, -1, -1):
                tags[k] = bp[(2 + k, tags[1 + k], tags[2 + k])]

            result.append([])
            for key in sorted(tags):
                result[row].append(tags[key])

        return result
