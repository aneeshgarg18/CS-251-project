from pattern.en import lexeme
from nltk.data import find
from bllipparser import RerankingParser
import urllib
import requests
from .helper import *

sentence = "He were very fast."

def obtain_tags(sentence):
	model_dir = find('models/bllip_wsj_no_aux').path
	parser = RerankingParser.from_unified_model_dir(model_dir)

	best = parser.parse(sentence)
	tree0 = str(best.get_reranker_best())
	tree1 = str(best.get_parser_best())

	open_index = 0
	close_index = -1
	tags0 = []
	for index in range(len(tree0)):
		if tree0[index] == '(':
			open_index = index
		elif tree0[index] == ')':
			if open_index > close_index:
				tags0.append(tuple(reversed(tree0[open_index + 1:index].split())))
			close_index = index

	open_index = 0
	close_index = -1
	tags1 = []
	for index in range(len(tree1)):
		if tree1[index] == '(':
			open_index = index
		elif tree1[index] == ')':
			if open_index > close_index:
				tags1.append(tuple(reversed(tree1[open_index + 1:index].split())))
			close_index = index
	final = []
	for index in range(len(tags0)):
		if tags0[index][1] == 'JJ':
			final.append(tags0[index])
		elif tags1[index][1] == 'JJ':
			final.append(tags1[index])
		else:
			final.append(tags0[index])
	return final

def Tense_Checker(sentence):
	lst = obtain_tags(sentence)
	print(lst)
	errors = []

	for index in range(len(lst)):
		if lst[index][1][:2] == 'VB':
			possible = lexeme(lst[index][0].lower())
			if index == 0 and lst[1][0][0].isalpha():
				temp = []
				for word in possible:
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
				for word in possible:
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
					for word in possible:
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
					for word in possible:
						encoded_query = urllib.parse.quote(lst[index - 1][0].lower() + ' ' + word.lower())
						params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3, 'format': 'tsv'}
						params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
						response = requests.get('https://api.phrasefinder.io/search?' + params)
						try:
							temp.append((int(response.text.split()[3]), word))
						except:
							temp.append((0, word))

			elif lst[index + 1][0][0].isalpha():
				for word in possible:
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