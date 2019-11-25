#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 16:34:32 2019

@author: aneesh
"""

import nltk
#from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize,sent_tokenize
import requests


def synonym(sent):
    ret_lst = []
    word_list = word_tokenize(sent)
    l = len(word_list)
    tagged = nltk.pos_tag(word_list)
    for i in range(0,l):
        word = word_list[i]
        tag2 = tagged[i][1][:2]
        tag3 = tagged[i][1][:3]
        con = 0
        if tag2 == "JJ":
            con = 1
        elif tag2 == "RB":
            con = 1 
        elif tag2 == "VB":
            con = 1 
        elif tag2 == "NN":
            if tag3 == "NNP":
                continue
            con = 1
        if con == 0:
            continue
#        print(word)
        lst=[]
        link='https://api.datamuse.com/words?rel_syn='
        link = link+word
        if i>0:
            if len(word_list[i-1])>1:
                link = link+'&lc='+word_list[i-1]
        if i<(l-1):
            if len(word_list[i+1])>1:
                link = link+'&rc='+word_list[i+1]
        link = link+'&max=5'
        response = requests.get(link)
        assert response.status_code == 200
        for d in response.json():
            lst.append(d['word'])
        if len(lst)>0:
            ret_lst.append((i,lst))
    return ret_lst

#text = "This is a big dog. the cat was fighting the dog. Who is responsible for completing this project?"
#sent_list = sent_tokenize(text)
#for sent  in sent_list:
#    l = synonym(sent)
#    print(l)