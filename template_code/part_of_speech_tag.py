# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 13:19:39 2018

@author: Erik
"""
import nltk
from pos_translation import pos_dict
sentence = "At eight o'clock on Thursday morning Arthur didn't feel very good."
tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens)

for tag in tagged:
    print(tag) # print raw tag
    print("   " + tag[1] + ": " + pos_dict[tag[1]]) #print tag translation