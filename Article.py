#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 13:58:31 2019

@author: pranavg
"""

import itertools
import re

sent = "Give me an hour.\n"

try:
    from future_builtins import map, zip
except ImportError: # Python 3 (or old Python versions)
    map, zip = map, zip
from operator import methodcaller

import nltk  # $ pip install nltk
from nltk.corpus import cmudict  # >>> nltk.download('cmudict')

def starts_with_vowel_sound(word, pronunciations=cmudict.dict()):
    for syllables in pronunciations.get(word, []):
        return syllables[0][-1].isdigit()  # use only the first one

def check_a_an_usage(words):
    print(words)
    # iterate over words pairwise (recipe from itertools)
    #note: ignore Unicode case-folding (`.casefold()`)
    l = []
    a, b = itertools.tee(map(methodcaller('lower'), words)) 
    next(b, None)
    for a, w in zip(a, b):
        if (a == 'a' or a == 'an') and re.match('\w+$', w): 
            valid = (a == 'an') if starts_with_vowel_sound(w) else (a == 'a')
            print(valid, a, w)
            l.append((valid, a, w))
        else:
            l.append((True, a, w))
    sent = ''
    for index in range(len(l)):
        if l[index][0]:
            sent = sent + words[index] + ' '
        else:
            if len(words[index]) == 1:
                sent = sent + words[index] + 'n '
            else:
                sent = sent + words[index][0] + ' '
    sent = sent[:-1]
    sent = sent + words[-1]
    print(sent)
    return l
#note: you could use nltk to split text in paragraphs,sentences, words
pairs = ((a, w)
         for sentence in [sent] if sentence.strip() 
         for valid, a, w in check_a_an_usage(nltk.wordpunct_tokenize(sentence))
         if not valid)

print("Invalid indefinite article usage:")
print('\n'.join(map(" ".join, pairs)))