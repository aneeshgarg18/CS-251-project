from nltk.tokenize import word_tokenize
from nltk import pos_tag
import urllib
import requests
from .helper import *

sentence = "Who is responsible for this product?"

def Interrogative_Checker(sentence):
	lst = pos_tag(word_tokenize(sentence))
	print(lst)

	errors = []
	pronouns = ['what', 'when', 'why', 'where', 'which', 'who', 'whose', 'whom', 'how']
	for index in range(len(lst)):
		if lst[index][0].lower() in pronouns:
			count = 2
			string = ''
			try:
				if lst[index + 1][0][0].isalpha():
					string += ' ' + lst[index + 1][0].lower()
					count += 1
					if lst[index + 2][0][0].isalpha():
						string += ' ' + lst[index + 2][0].lower()
						count += 1
						if lst[index + 3][0][0].isalpha():
							string += ' ' + lst[index + 3][0].lower()
							count += 1
			except:
				pass
			
			temp = []
			for pronoun in pronouns:
				encoded_query = urllib.parse.quote(pronoun + string)
				params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3, 'format': 'tsv'}
				params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
				response = requests.get('https://api.phrasefinder.io/search?' + params)
				try:
					temp.append((int(response.text.split()[count]), pronoun))
				except:
					temp.append((0, pronoun))

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

	return convert(errors)