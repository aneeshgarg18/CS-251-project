#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 00:45:53 2019

@author: pranavg
"""

import nltk
import os
import nltk.corpus
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import words

from nltk.data import load

# sent = "Nature is that long-lasting and physical world that surrounds us and makes life possible on earth. Nature is the heart of earth. Nature heals us and helps build connection with our freedom, authenticity and our souls. Simply connecting and feeling nature gives us a divine pleasure. We have a strong bond and emotional connection with nature. The serenity of nature calms our hearts. The stillness and movement in nature both have a hypnotizing effect. The unfolding creativity of nature is an art. It is alluring to experience solitude with nature. The practice of devoting ourselves to the bliss of nature is soothing and reviving. Everyone loves to escape away in the mysteries of nature."
sent1 = "What a bright day!"
# sent_tokens = word_tokenize(sent)

lst1 = nltk.pos_tag(word_tokenize(sent1))
# lst = nltk.pos_tag(sent_tokens)
# print(lst1)
#print()
#print()
# dictionary = words.words()
#for word in dictionary:
#    print(word)
# print(lst1)
# for pair in lst:
#     if pair[1] == 'DT':
#         print(pair[0])
        
# import pattern.en

def space_needed(token):
	if token[1] == '.' or token[0] == "n't":
		return ''
	return ' '

def convert(tokens_list, corrupted_indices):
	"""
	tokens_list -> Simply the nltk.pos_tag(word_tokenize())
	corrupted_indices -> List of tuples, each tuple has index w.r.t token_list and list of suggestions.
	"""
	if len(tokens_list) == 0:
		return []
	ans = []
	ind = [pair[0] for pair in corrupted_indices]
	current_index = 0
	try:
		if corrupted_indices[0][0] == 0:
			ans.append((tokens_list[0][0], corrupted_indices[0][1]))
			current_index = 1
	except:
		pass
	tokens_mod = []
	string = ''
	if current_index == 0:
		string += tokens_list[0][0]
	for index in range(1, len(tokens_list)):
		if index in ind:
			ans.append((string + space_needed(tokens_list[index]), []))
			ans.append((tokens_list[index][0], corrupted_indices[current_index][1]))
			current_index += 1
			string = ''
		else:
			string += space_needed(tokens_list[index]) + tokens_list[index][0]
	if string != '':
		ans.append((string + space_needed(tokens_list[index]), []))
	return ans
