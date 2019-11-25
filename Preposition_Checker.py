from nltk import pos_tag
from nltk.tokenize import word_tokenize
import urllib
import requests
from .helper import *

sent="On what time does the train arrive?"
sent1 = "A sun is very bright. There is an person standing in a driveway. Aneesh is an temporary guy. I am shocked."

def Preposition_Checker(sentence):
    lst = pos_tag(word_tokenize(sentence))

    print(lst)
    errors = []

    prepositions = ['on', 'in', 'at']
    for index in range(len(lst)):
        if lst[index][0].lower() in prepositions:
            count = 1
            indi = 0
            if index > 0 and lst[index - 1][0][0].isalpha():
                front = lst[index - 1][0].lower() + ' '
                count += 1
                indi = 1
            else:
                front = ''
            if index < len(lst) - 1 and lst[index + 1][0][0].isalpha():
                back = ' ' + lst[index + 1][0].lower()
                count += 1
                if index < len(lst) - 2 and lst[index + 2][0][0].isalpha():
                    back += ' ' + lst[index + 2][0].lower()
                    count += 1
            else:
                back = ''

            l = []
            for preposition in prepositions:
                encoded_query = urllib.parse.quote(front + preposition + back)
                params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3, 'format': 'tsv'}
                params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
                response = requests.get('https://api.phrasefinder.io/search?' + params)
                try:
                    l.append((int(response.text.split()[count + indi + 1]), preposition))
                except:
                    l.append((0, preposition))
            print(l)
            l.sort()
            if lst[index][0][0].isupper():
                l = [(pair[0], pair[1][0].upper() + pair[1][1:]) for pair in l]
            max_frequency = l[-1][0]
            for pair in l:
                if lst[index][0] == pair[1]:
                    current_frequency = pair[0]
            if max_frequency <= 5 * current_frequency:
                continue
            else:
                suggestions = []
                for ind in range(len(l) - 1, -1, -1):
                    if l[ind][1] != lst[index][0] and l[ind][0] * 5 > max_frequency:
                        suggestions.append(l[ind][1])
                errors.append((index, suggestions))

    return convert(lst, errors)
            
# print(Preposition_Checker(sent))