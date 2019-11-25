from nltk import edit_distance, FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import words, brown

brown_text = []
for c in brown.categories():
    for w in brown.words(categories = c):
        brown_text.append(w)

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
#                    print(word)
#                    print(['a','i'])
                    suggested_list.append('a')
                    suggested_list.append("i")
            pass
#        elif word in words.words() or ((word[:1].lower()+word[1:]) in words.words() and w==0):
#            pass
        elif (word[:1].lower() + word[1:]) in words.words():
            pass
        elif word.lower() in words.words():
#            print(word)
#            print(word[:1]+word[1:].lower())
            suggested_list.append(word[:1] + word[1:].lower())
        else:
#            print("1")
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
#        new_list=[]
#        for x in new:
#            new_list.append(x)
        if len(new_list)>0:
            lst.append((w, new_list))
    return lst
#                print(word)
#                print(new_list)
    


#text ='The tool should be able to How run for ab large text, "Hey there"'" and note that it should don't run for a given sentence in the text only once a full stop, question mark or an exclamation mark is detected. For e.g. Why is responsible for completing this prodect? It is vry good"
#text = 'It is very bad thingj.'
#print(sent_tokenize(text))
#print(word_tokenize(text))
#print(edit_distance("Natbr","nature"))

#def edit_with_distance(wd,d):
#    if (d==0):
#        return wd
#    else:
#        

#max_int = 0
#for word in words.words():
#    max_int = max(max_int, len(word))
#print(max_int)
dictionary = []
dictionary_lowercase = []
for i in range(24):
    dictionary.append([])
    dictionary_lowercase.append([])
for word in words.words():
    l = len(word)
    dictionary[l-1].append(word)
    dictionary_lowercase[l-1].append(word.lower())

#sent_list = sent_tokenize(text)
#for sent in sent_list:
#    l=spell_check(sent)
#    print(l)
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
