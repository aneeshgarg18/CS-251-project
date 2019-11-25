from nltk import edit_distance, FreqDist, pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import words, brown
from .helper import *

brown_text = []
dictionary = []
dictionary_lowercase = []
# def spell(text):
    # brown_text = []
for c in brown.categories():
    for w in brown.words(categories = c):
        brown_text.append(w)
# dictionary = []
# dictionary_lowercase = []
for i in range(24):
    dictionary.append([])
    dictionary_lowercase.append([])
for word in words.words():
    l = len(word)
    dictionary[l-1].append(word)
    dictionary_lowercase[l-1].append(word.lower())
# return spell_check(text)

def unigrams(s):
    return FreqDist(brown_text)[s]
    
def sort_freq(l):
    lst=[]
    for x in l:
        f = unigrams(x)
        lst.append((f,x))
    lst = list(set(lst))
    lst.sort()
    suggestions = []
    if not lst:
        return []
    for index in range(len(lst) - 1, -1, -1):
        if lst[index][0] > 10:
            suggestions.append(lst[index][1])
    return suggestions

def spell_check(sent):
    lst = []
    word_list = word_tokenize(sent)
    for w in range(len(word_list)):
        suggested_list = []
        word = word_list[w]
        if len(word) == 1:
            if word.isalpha():
                if word.lower() != 'a' and word.lower() != 'i':
                    suggested_list.append('a')
                    suggested_list.append("i")
            pass
        elif (word[:1].lower() + word[1:]) in words.words():
            pass
        elif word.lower() in words.words():
            suggested_list.append(word[:1] + word[1:].lower())
        else:
            flag = 1
            l = len(word)
            no_of_letters = 0
            for letter in word:
                if letter.isalpha():
                    no_of_letters += 1
            if no_of_letters == 0:
                flag = 0
            elif no_of_letters == l - 1:
                for i in range(len(word)):
                    if i < l - 1 and word[i] == "'":
                        if (word[:i] + "o" + word[i + 1:]) in words.words():
                            flag = 0
            if flag == 1:
                for i in range(3):
                    for j in range(len(dictionary_lowercase[l - i])):
                        d_word = dictionary_lowercase[l - i][j]
                        if edit_distance(d_word,word.lower()) < 2:
                            if w == 0:
                                suggested_list.append(d_word[:1].upper() + d_word[1:])
                            else:
                                suggested_list.append(dictionary[l - i][j])
                if len(suggested_list) < 5:
                    for i in [-1, 3]:
                        for j in range(len(dictionary_lowercase[l - i])):
                            d_word = dictionary_lowercase[l - i][j]
                            if edit_distance(d_word, word.lower())<2:
                                if w == 0:
                                    suggested_list.append(d_word[:1].upper() + d_word[1:])
                                else:
                                    suggested_list.append(dictionary[l - i][j])
        new_list = sort_freq(suggested_list)
        if len(new_list)>0:
            lst.append((w, new_list))
    return convert(pos_tag(word_list), lst);

# text = 'This prodect is vry gud.'
# print(spell(text))
