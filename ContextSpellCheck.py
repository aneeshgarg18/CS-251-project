import urllib
import requests
from nltk import pos_tag, edit_distance, FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import words, brown
from helper import *
import pickle

lingo = {'arbit':'arbitrary', 'bandi':'girl', 'enthu':'enthusiasm', 'infi':'infinite', 'insti':'institute', 'liby':'library', 'sophie':'sophomore', 'bc':'branch change'}

with open ('dictionary.pickle','rb') as fp:
    dictionary = pickle.load(fp)
with open ('dictionary_lowercase.pickle','rb') as fp:
    dictionary_lowercase = pickle.load(fp)
with open ('brown_text.pickle','rb') as fp:
    brown_text = pickle.load(fp)

def unigrams(s):
    return FreqDist(brown_text)[s]

def spell_context(sent):
    clst = []
    word_list = word_tokenize(sent)
    for w in range(len(word_list)):
        word = word_list[w]
        l = len(word)
        temp=""
        mx=0
        if word.lower() in list(lingo.keys()):
            temp = lingo[word]
            mx = unigrams(word)
        if l<4:
            clst.append(None)
            continue
        if l>1:
            for d in dictionary_lowercase[l-2]:
                if edit_distance(word.lower(),d)<=1:
                    if unigrams(d)>mx:
                        temp = d
                        mx = unigrams(d)
        for d in dictionary_lowercase[l-1]:
            if edit_distance(word.lower(),d)<=1:
                if unigrams(d)>mx:
                    temp = d
                    mx = unigrams(d)
        if l<33:
            for d in dictionary_lowercase[l]:
                if edit_distance(word.lower(),d)<=1:
                    if unigrams(d)>mx:
                        temp = d
                        mx = unigrams(d)
        clst.append(temp)
    return clst

def SpellCheck(sentence):
	l = spell_context(sentence)
	lst = pos_tag(word_tokenize(sentence))
	print(lst)
	errors = []

	for index in range(len(lst)):
		if not lst[index][0][0].isalpha():
			continue
		if l[index] is None:
			continue
		count = 1
		if index > 0 and lst[index - 1][0][0].isalpha():
			front = lst[index - 1][0].lower() + ' '
			count += 1
		else:
			front = ''
		if index < len(lst) - 1 and lst[index + 1][0][0].isalpha():
			back = ' ' + lst[index + 1][0].lower()
			count += 1
		else:
			back = ''

		# print(front + lst[index][0].lower() + back)
		encoded_query = urllib.parse.quote(front + lst[index][0].lower() + back)
		params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3, 'format': 'tsv'}
		params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
		response = requests.get('https://api.phrasefinder.io/search?' + params)
		try:
			freq = int(response.text.split()[count])
		except:
			freq = 0

		# print(front + l[index].lower() + back)
		encoded_query = urllib.parse.quote(front + l[index].lower() + back)
		params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3, 'format': 'tsv'}
		params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
		response = requests.get('https://api.phrasefinder.io/search?' + params)
		try:
			proposed_freq = int(response.text.split()[count])
		except:
			proposed_freq = 0

		# print(freq, proposed_freq)
		if freq * 10 < proposed_freq:
			if lst[index][0][0].isupper():
				errors.append((index, [l[index][0].upper() + l[index][1:]]))
			else:
				errors.append((index, [l[index]]))
	return convert(lst, errors)

# sent = 'This is vary good.'
# print(SpellCheck(sent, spell_context(sent)))