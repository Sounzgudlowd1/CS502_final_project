# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 13:19:39 2018

@author: Erik
"""
import nltk
from itertools import chain
sentence = "At eight o'clock on Thursday morning Arthur didn't feel very good."
tokens = nltk.word_tokenize(sentence)

unigrams = nltk.ngrams(tokens,1) 
bigrams = nltk.ngrams(tokens, 2)
grams = chain(unigrams, bigrams)
for gram in grams:
    print(gram)