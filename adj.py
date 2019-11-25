
import nltk
from nltk.tokenize import word_tokenize,sent_tokenize
import urllib
import requests
from nltk.data import find
from bllipparser import RerankingParser
model_dir = find('models/bllip_wsj_no_aux').path
parser = RerankingParser.from_unified_model_dir(model_dir)

def bigrams(s):
    encoded_query = urllib.parse.quote(s)
    params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3, 'format': 'tsv'}
    params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
    response = requests.get('https://api.phrasefinder.io/search?' + params)
    assert response.status_code == 200
    lst = response.text.split()
    if len(lst)>0:
        return lst[2]
    else:
        return 0

def trigrams(s):
    encoded_query = urllib.parse.quote(s)
    params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3, 'format': 'tsv'}
    params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
    response = requests.get('https://api.phrasefinder.io/search?' + params)
    assert response.status_code == 200
    lst = response.text.split()
    if len(lst)>0:
        return lst[3]
    else:
        return 0

def obtain_tags(sentence):
    

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

def adjective(sent):
    lst=[]
    word_list = word_tokenize(sent)
    tagged = obtain_tags(sent)
#    print(tagged)
    i=1
    while i<len(tagged):
        tag1 = tagged[i-1][1][:2]
        if tag1!="JJ":
            i=i+1
            continue
        tag2 = tagged[i][1][:2]
        if tag1==tag2:
            w1 = word_list[i-1].lower()
            w2 = word_list[i].lower()
            tag3 = tagged[i+1][1][:2]
            if tag3==tag2:
                # print(i)
                # print(tag1)
                # print(tag2)
                # print(tag3)
                i_list=[i-1,i,i+1]
                w3 = word_list[i+1].lower()
                s1 = w1+" "+w2
                r1 = w2+" "+w1
                s2 = w1+" "+w3
                r2 = w3+" "+w1
                s3 = w2+" "+w3
                r3 = w3+" "+w2
                st1 = int(bigrams(s1))
                rt1 = int(bigrams(r1))
                st2 = int(bigrams(s2))
                rt2 = int(bigrams(r2))
                st3 = int(bigrams(s3))
                rt3 = int(bigrams(r3))
                if rt1>5*st1:
                    if rt2>5*st2:
                        if rt3>5*st3:
                            lst.append((i_list,[w3+" "+w2+" "+w1]))
                        else:
                            lst.append((i_list,[w2+" "+w3+" "+w1]))
                    else:
                        lst.append((i_list,[w2+" "+w1+" "+w3]))
                else:
                    if rt2>5*st2:
                        lst.append((i_list,[w3+" "+w1+" "+w2]))
                    else:
                        if rt3>5*st3:
                            lst.append((i_list,[w1+" "+w3+" "+w2]))
                # s4 = w2+" "+w3+" "+w1
                # s5 = w3+" "+w1+" "+w2
                # s6 = w3+" "+w2+" "+w1
                # t=[]
                # tr = trigrams(s1)
                # t.append((tr,s1))
                # t.append((trigrams(s2),s2))
                # t.append((trigrams(s3),s3))
                # t.append((trigrams(s4),s4))
                # t.append((trigrams(s5),s5))
                # t.append((trigrams(s6),s6))
                # t.sort(reverse=True)
                # temp=[]
                # for x in t:
                #     if x[1]==s1:
                #         break
                #     if x[0]>5*tr:
                #        temp.append(x[1])
                # if len(temp)>0:
                #     print(1)
                #     lst.append(([i-1,i,i+1],temp))
                # print("hi")
                i = i+3
            else:
                # print(i)
                s = w1+ " " + w2
                r = w2 + " " +w1
                st = int(bigrams(s))
                # print(st)
                rt = int(bigrams(r))
                if rt>5*st:
                    lst.append(([i-1,i],[r]))
                i = i+2
        else:
            i = i+1
    return lst

text = 'I bought blue new bike. I also bought a red new huge vehicle.'

sent_list = sent_tokenize(text)
# print(sent_list)
for sent in sent_list:
    l=adjective(sent)
    print(l)
    # print(sent)



#                    print(s)
#                    print(r)
#        tag3=""
#        if i<(len(tagged)-1):
#            tag3 = tagged[i+1][1][:2]
#        if tag3==tag2:
#            pass
#        else:
#            lc = word_list[i-2]
#            lcp=0
#            if lc.replace("'","").isalpha():
#                lcp=1
#            rc = word_list[i+1]
#            rcp=0
#            if rc.replace("'","").isalpha():
#                rcp=1
#            lt1=1
#            lt2=1
#            rt1=1
#            rt2=1
#            if lcp:
#                lt1 = trigrams(word_list[i-2].lower()+" "+s)
#                lt2 = trigrams(word_list[i-2].lower()+" "+word_list[i].lower()+" "+word_list[i-1].lower())
#            if rcp:
#                rt1 = trigrams(s+" "+word_list[i+1].lower())
#                rt2 = trigrams(word_list[i].lower()+" "+word_list[i-1].lower()+" "+word_list[i+2].lower())
#            print(lt1)
#            print(lt2)
#            print(rt1)
#            print(rt2)
#            if rt2>5*rt1:
#                print(s)
#                print(r)
#            else:
#                if rt2>rt1 and rt2*lt2>lt2*lt1:
#                    print(s)
#                    print(r)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
