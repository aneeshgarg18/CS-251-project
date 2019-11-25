from nltk import edit_distance, FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import words, brown
import pickle
from .helper import *
with open ('dictionary.pickle','rb') as fp:
    dictionary=pickle.load(fp)
with open ('dictionary_lowercase.pickle','rb') as fp:
    dictionary_lowercase=pickle.load(fp)
with open ('brown_text.pickle','rb') as fp:
    brown_text = pickle.load(fp)


lingo = {'arbit':'arbitrary', 'bandi':'girl', 'enthu':'enthusiasm', 'infi':'infinite', 'insti':'institute', 'liby':'library', 'sophie':'sophomore', 'bc':'branch change'}
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

def spell_check(sent):
    lst = []
    word_list = word_tokenize(sent)
    for w in range(len(word_list)):
        suggested_list = []
        word = word_list[w]
        l = len(word)
        if word.lower() in list(lingo.keys()):
            suggested_list.append(lingo[word])
        elif l == 1:
            if word.isalpha():
                if word.lower() != 'a' and word.lower() != 'i':
                    suggested_list.append('a')
                    suggested_list.append("i")
            pass
        elif (word[:1].lower() + word[1:]) in dictionary[l-1]:
            pass
        elif word.lower() in dictionary[l-1]:
            suggested_list.append(word[:1] + word[1:].lower())
        else:
            flag = 1
            no_of_letters = 0
            for letter in word:
                if letter.isalpha():
                    no_of_letters += 1
            if no_of_letters == 0:
                flag = 0
            elif no_of_letters == l - 1:
                for i in range(len(word)):
                    if i < l - 1 and word[i] == "'":
                        if (word[:i] + "o" + word[i + 1:]) in dictionary[l-1]:
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
    return convert(pos_tag(word_list), lst)
    


#text ='The tool should be able to How run for ab large text, "Hey there"'" and note that it should don't run for a given sentence in the text only once a full stop, question mark or an exclamation mark is detected. For e.g. Why is responsible for completing this prodect? It is vry good"
# text = 'He has infi money.'
# sent_list = sent_tokenize(text)
# for sent in sent_list:
#     l=spell_check(sent)
#     l1 = spell_context(sent)
#     print(l)
#     print(l1)

#dictionary = []
#dictionary_lowercase = []
#for i in range(33):
#    dictionary.append([])
#    dictionary_lowercase.append([])
#for i in range(len(brown_text)):
#    word = brown_text[i]
#    l = len(word)
#    if word not in dictionary[l-1]:
#        dictionary[l-1].append(word)
#        dictionary_lowercase[l-1].append(word.lower())
#with open('dictionary.pickle', 'wb') as fp:
#    pickle.dump(dictionary,fp)
#with open('dictionary_lowercase.pickle', 'wb') as fp:
#    pickle.dump(dictionary_lowercase,fp)
    



#    word_list = word_tokenize(sent)
#    for w in range(len(word_list)):
#        word = word_list[w]
#        if len(word)==1:
#            if word.isalpha():
#                if word!='a' and word!='i':
#                    print(word)
#                    print(['a','i'])
#            pass
##        elif word in words.words() or ((word[:1].lower()+word[1:]) in words.words() and w==0):
##            pass
#        elif (word[:1].lower()+word[1:]) in words.words():
#            pass
#        elif word.lower() in words.words():
#            print(word)
#            print(word[:1]+word[1:].lower())
#        else:
##            print("1")
#            flag=1
#            suggested_list=[]
#            l = len(word)
#            no_of_letters = 0
#            for letter in word:
#                if letter.isalpha():
#                    no_of_letters+=1
#            if no_of_letters == 0:
#                flag=0
#            elif no_of_letters == l-1:
#                for i in range(len(word)):
#                    if i<l-1 and word[i]=="'":
#                        if (word[:i]+"o"+word[i+1:]) in words.words():
#                            flag=0
#            if flag==1:
#                for i in range(3):
#                    for j in range(len(dictionary_lowercase[l-i])):
#                        d_word = dictionary_lowercase[l-i][j]
#                        if edit_distance(d_word,word.lower())<2:
#                            if w==0:
#                                suggested_list.append(d_word[:1].upper()+d_word[1:])
#                            else:
#                                suggested_list.append(dictionary[l-i][j])
#                if len(suggested_list) < 5:
#                    for i in [-1,3]:
#                        for j in range(len(dictionary_lowercase[l-i])):
#                            d_word = dictionary_lowercase[l-i][j]
#                            if edit_distance(d_word,word.lower())<2:
#                                if w==0:
#                                    suggested_list.append(d_word[:1].upper()+d_word[1:])
#                                else:
#                                    suggested_list.append(dictionary[l-i][j])
#                print(word)
#                print(suggested_list)
