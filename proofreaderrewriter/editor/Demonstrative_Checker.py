from nltk.tokenize import word_tokenize
from nltk import pos_tag
import urllib
import requests
from .helper import *

sentence = "It seems that that is a bad situation."

def Demonstrative_Checker(sentence):
	lst = pos_tag(word_tokenize(sentence))
	print(lst)

	errors = []
	pronouns = ['this', 'that', 'these', 'those']
	for index in range(len(lst)):
		if lst[index][0].lower() in pronouns:
			if index == 0 and lst[1][0][0].isalpha():
				temp = []
				for word in pronouns:
					encoded_query = urllib.parse.quote(word.lower() + ' ' + lst[1][0].lower())
					params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3, 'format': 'tsv'}
					params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
					response = requests.get('https://api.phrasefinder.io/search?' + params)
					try:
						temp.append((int(response.text.split()[3]), word))
					except:
						temp.append((0, word))

			elif index == len(lst) - 1 and lst[index - 1][0][0].isalpha():
				temp = []
				for word in pronouns:
					encoded_query = urllib.parse.quote(lst[index - 1][0].lower() + ' ' + word.lower())
					params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3, 'format': 'tsv'}
					params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
					response = requests.get('https://api.phrasefinder.io/search?' + params)
					try:
						temp.append((int(response.text.split()[3]), word))
					except:
						temp.append((0, word))

			elif lst[index - 1][0][0].isalpha():
				if lst[index + 1][0][0].isalpha():
					temp = []
					for word in pronouns:
						encoded_query = urllib.parse.quote(lst[index - 1][0].lower() + ' ' + word.lower() + ' ' + lst[index + 1][0].lower())
						params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3, 'format': 'tsv'}
						params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
						response = requests.get('https://api.phrasefinder.io/search?' + params)
						try:
							temp.append((int(response.text.split()[3]), word))
						except:
							temp.append((0, word))
				else:
					temp = []
					for word in pronouns:
						encoded_query = urllib.parse.quote(lst[index - 1][0].lower() + ' ' + word.lower())
						params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3, 'format': 'tsv'}
						params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
						response = requests.get('https://api.phrasefinder.io/search?' + params)
						try:
							temp.append((int(response.text.split()[3]), word))
						except:
							temp.append((0, word))

			elif lst[index + 1][0][0].isalpha():
				for word in pronouns:
					temp = []
					encoded_query = urllib.parse.quote(word.lower() + ' ' + lst[index + 1][0].lower())
					params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3, 'format': 'tsv'}
					params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
					response = requests.get('https://api.phrasefinder.io/search?' + params)
					try:
						temp.append((int(response.text.split()[3]), word))
					except:
						temp.append((0, word))
			temp.sort()
			print(temp)
			if lst[index][0][0].isupper():
				temp = [(pair[0], pair[1][0].upper() + pair[1][1:]) for pair in temp]
			max_frequency = temp[-1][0]
			for pair in temp:
				if lst[index][0] == pair[1]:
					current_frequency = pair[0]
			if max_frequency <= 5 * current_frequency:
				continue
			else:
				suggestions = []
				for ind in range(len(temp) - 1, -1, -1):
					if temp[ind][1] != lst[index][0] and temp[ind][0] * 5 > max_frequency:
						suggestions.append(temp[ind][1])
				errors.append((index, suggestions))
	return convert(lst, errors)