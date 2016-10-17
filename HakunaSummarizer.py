
# coding: utf-8

# In[2]:

from BeautifulSoup import BeautifulSoup
import nltk as nltk
from nltk.corpus import stopwords
import re
import numpy as np
import pickle
import copy
import json
from collections import defaultdict
import webbrowser
import sys


# In[23]:
filename = sys.argv[1]
#f = open('/home/pragati/holdoutHalf/06_3.xml', 'r')
f = open(filename, 'r')
num_sent = int(sys.argv[2])
text_full = f.read()
soup = BeautifulSoup(text_full) 


# In[24]:

with open("/home/pragati/Git_Pragati/RTC-Document_Summarization/imp_dict.dat",'r') as p:
    imp_dict = pickle.load(p)
imp_pick=imp_dict.keys()


# In[25]:

glob_text = soup('sentences')[0].text.split('\n')
curated_glob = [sent.lstrip('0123456789.-" ') for sent in glob_text if len(sent) > 10]


# In[26]:

text = []
i_range = len(curated_glob)
copy_curated = copy.copy(curated_glob)
for i in range(i_range):
    tokens = [w.lower() for w in copy_curated[i].split()]
    punc_rem = [re.sub('[^A-Za-z]+', '', word) for word in tokens]
    #lemmatized = [lemm.lemmatize(w) for w in punc_rem]
    filt_stop = [word for word in punc_rem if word not in stopwords.words('english')]
    if len(filt_stop) < 10:
        to_rem = copy_curated[i]
        curated_glob.remove(to_rem)
    else:
        text.append(filt_stop)


# In[27]:

def intersection_comp(s_1, s_2):
    s1 = set(s_1)
    s2 = set(s_2)
    if (len(s1) + len(s2)) == 0:
        return 0
    else:
        # We normalize the result by the average number of words
        return len(s1.intersection(s2)) / float(((len(s1) + len(s2)) / 2))
def intersection_corpus(s_1):
    s1 = set(s_1)
    s2 = set(imp_pick)
    if len(s1) == 0:
        return 0
    else:
        return len(s1.intersection(s2)) / float(len(s1))


# In[28]:

n = len(text)
values = np.zeros((n,n+1), dtype = np.double)
for i in range(0, n):
    for j in range(0, n):
        values[i][j] = intersection_comp(text[i], text[j])
    values[i][n] = intersection_corpus(text[i])


# In[29]:

score_list = []
for i in range(0, n):
    score = 0
    for j in range(0, n):
        if i == j:
            continue
        score += values[i][j]
    score_list.append(score)


# In[30]:

keys =[]
text_dict = {}
norm_score = [float(i)/max(score_list) for i in score_list]
for i in range(0,n):
    final = (0.3* norm_score[i]) + (0.7 * values[i][n])
    #final = (values[i][n])
    keys.append(" ".join(text[i]))
    text_dict[" ".join(text[i])] = final


# In[31]:

set_summary =[]
set_tokensent=[]
thresh = np.sort(text_dict.values())[::-1][:num_sent][num_sent-1]
for i in range(n):
    if text_dict[keys[i]] >= thresh:
        to_append1 = str(re.sub('[^A-Za-z0-9]+', ' ', curated_glob[i].lstrip('0123456789.- ')))
        set_summary.append(to_append1)
        set_tokensent.append(" ".join(text[i]))
#summary = list(set(set_summary))
#summary_token = list(set(set_tokensent))
#for j in range(len(set_summary)):
#    print set_summary[j], ".\n"


# In[32]:

dict_key = defaultdict(list)
num_iter = len(set_tokensent)
for i in range(num_iter):
    sel_word = 'other'
    max_rank = 0
    for word in set_tokensent[i].split():
        if word in imp_pick:
            rank = imp_dict[word]
            if rank>max_rank:
                max_rank = rank
                sel_word = word
    dict_key[sel_word].append(set_summary[i])
            
            


# In[33]:

def write(data):
    print('Creating new json file') 
    name = '/home/pragati/HACK101/flare.json'  # Name of text file coerced with +.txt
    with open(name, 'w') as outfile:
        json.dump(data, outfile)


# In[34]:

def createJson(summary):
    jsonObj = {}
    jsonObj["name"] = "Document"
    children = []
    for key,value in summary.iteritems():
        catchsent=[]
        for sentence in value:
            catchsent.append({"name" : sentence,"size" : 3219})
        children.append({"name" : key,"children" : catchsent})
    jsonObj["children"]=children
    return jsonObj


# In[35]:

jsonObj=createJson(dict_key)


# In[36]:

write(jsonObj)


# In[37]:

filename = '/home/pragati/HACK101/index.html'
webbrowser.open_new_tab(filename)


# In[ ]:



