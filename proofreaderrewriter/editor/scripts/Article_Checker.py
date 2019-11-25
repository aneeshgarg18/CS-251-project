from nltk import pos_tag
from nltk.tokenize import word_tokenize
import urllib
import requests
from .helper import *

sent = "A sun is very bright. There is an person standing in a driveway. Aneesh is an temporary guy. I am shocked."

def Article_Checker(sentence):
    lst = pos_tag(word_tokenize(sentence))

    print(lst)
    errors = []

    articles = ['a', 'an', 'the']
    for index in range(len(lst) - 1):
        if lst[index][0].lower() in articles and lst[index + 1][0][0].isalpha():
            l = []
            for article in articles:
                encoded_query = urllib.parse.quote(article + ' ' + lst[index + 1][0].lower())
                params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3, 'format': 'tsv'}
                params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
                response = requests.get('https://api.phrasefinder.io/search?' + params)
                try:
                    l.append((int(response.text.split()[2]), article))
                except:
                    pass
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
                    if l[ind][1] != lst[index][0]:
                        suggestions.append(l[ind][1])
                errors.append((index, suggestions))

    return convert(lst, errors)
                    