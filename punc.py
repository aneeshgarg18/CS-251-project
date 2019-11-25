#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 21:48:43 2019

@author: aneesh
"""

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk.corpus
from nltk.corpus import words
#nltk.download('nps_chat')
posts = nltk.corpus.nps_chat.xml_posts()[:10000]


def dialogue_act_features(post):
    features = {}
    for word in word_tokenize(post):
        features['contains({})'.format(word.lower())] = True
    return features


def punctuation(sent):
    lst=[]
    sen = sent[:(len(sent)-1)]
    sen = sen[:1].upper() + sen[1:]
    word_list = word_tokenize(sent)
    w = word_list[0]
    if not w[0].isupper():
        lst.append((0,[w[0].upper()+w[1:]]))
    l = len(word_list)
    for i in range(1,l):
        word = word_list[i]
        if (word not in words.words()) and (not word[0].isupper()) and (word.replace("'","").isalpha()):
#            print(word)
#            print(word[:1].upper()+word[1:])
            lst.append((i,[word[:1].upper()+word[1:]]))
    e = sent[(len(sent)-1):]
#    print(e)
    tag = classifier.classify(dialogue_act_features(sen))
#    str(tag)
    if tag[2:]!="Question":
#        print(1)
        if e=="." or e=="!":
            pass
        else:
#            print(sen+".")
            lst.append((l-1,["."]))
    elif tag[2:]=="Question":
        if e=="?":
            pass
        else:
#            print(sen+"?")
            lst.append((l-1,["?"]))
    return(lst)

featuresets = [(dialogue_act_features(post.text), post.get('class')) for post in posts]
size = int(len(featuresets) * 0.1)
train_set, test_set = featuresets[size:], featuresets[:size]
classifier = nltk.NaiveBayesClassifier.train(train_set)
#print(nltk.classify.accuracy(classifier, test_set))

#text = 'rohan bought the little tiny blue ball?'
#sent_list = sent_tokenize(text)
#for sent in sent_list:
#    l=punctuation(sent)
#    print(l)
    #print(classifier.classify(dialogue_act_features("How are you")))
#print(classifier.classify(dialogue_act_features("my naem is anmol")))
#print(classifier.classify(dialogue_act_features("what is your name")))
#print(classifier.classify(dialogue_act_features("wow that's amazing")))

#text1 = "A sun is very bright. There is an person standing in the driveway. Aneesh is an temporary guy. I am shocked."
#text2 = "My name is aneesh."
#lst = [list(pair) for pair in nltk.pos_tag(word_tokenize(text2))]
#print(lst)