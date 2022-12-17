#!/usr/bin/env python
# coding: utf-8

# In[19]:


get_ipython().system('pip install tflearn ')


# In[2]:


get_ipython().system('pip install tensorflow --upgrade')


# In[ ]:


import numpy as np 
#tflearn and tensroslow causing kernel to die
import tflearn
import tensorflow as tf


# In[17]:


import nltk 

nltk.download('punkt')

from nltk import word_tokenize,sent_tokenize

from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy as np 
import random
import json
import pickle
with open(r"/Users/ananyagoel/Desktop/DS 2002/intents.json") as file:
    data = json.load(file)

try:
    with open("data.pickle","rb") as f:
        words, labels, training, output = pickle.load(f)

except:
    words = []
    labels = []
    docs_x = []
    docs_y = []
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
            
        if intent["tag"] not in labels:
            labels.append(intent["tag"])


    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    labels = sorted(labels)

    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
               bag.append(1)
            else:
              bag.append(0)
    
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        
        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)
    
    with open("data.pickle","wb") as f:
        pickle.dump((words, labels, training, output), f)


# In[20]:


# pip install -U discord==1.7.3 pip install -U discord.py==1.7.3
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    
    return np.array(bag)


# In[2]:


#defining function to give appropriate response to user  
def give_response(tag):
    if tag=="Question 1":
        query1 = {"TYPE":"movie"}
        mydoc1 = collection.find(query1).sort("SCORE",-1).limit(5)
        for x in mydoc1:
            print(x["TITLE"],x["SCORE"])
            
    if tag=="Question 2":
        query2 = {"TYPE":"show"}
        mydoc2 = collection.find(query2).sort("SCORE",-1).limit(5)
        for x in mydoc2:
            print(x["TITLE"],x["SCORE"])
            
    if tag=="Question 3":
        query3 = { "MAIN_GENRE": "romance", "TYPE":"movie"}
        mydoc3 = collection.find(query3)
        for x in mydoc3:
            print(x['TITLE'])
            
    if tag=="Question 4":
        query4 = {"TYPE":"movie"}
        mydoc4 = collection.find(query4).sort("RELEASE_YEAR",-1).limit(1)
        for x in mydoc4:
            print(x["TITLE"],x["RELEASE_YEAR"])
            
    if tag=="Question 5":
        query5 = {"TYPE":"movie"}
        mydoc5 = collection.find(query5).sort("SCORE",-1).limit(1)
        for x in mydoc5:
            print(x["TITLE"],x["SCORE"])
            
    if tag=="Question 6":
        query6 = {"TYPE":"show"}
        mydoc6 = collection.find(query6).sort("SCORE",-1).limit(1)
        for x in mydoc6:
            print(x["TITLE"],x["SCORE"])
            
    if tag=="Question 7":
        query7 = { "MAIN_GENRE": "comedy", "TYPE":"movie"}
        mydoc7 = collection.find(query7)
        for x in mydoc7:
            print(x['TITLE'])
            
    if tag=="Question 8":
        query8 = { "MAIN_GENRE": "horror", "TYPE":"movie"}
        mydoc8 = collection.find(query8)
        for x in mydoc8:
            print(x['TITLE'])
            
    if tag=="Question 9":
        query9 = { "MAIN_GENRE": "scifi", "TYPE":"show"}
        mydoc9 = collection.find(query9)
        for x in mydoc9:
            print(x['TITLE'])
            
    if tag=="Question 10":
        query10 = { "MAIN_GENRE": "comedy", "TYPE":"show"}
        mydoc10 = collection.find(query10)
        for x in mydoc10:
            print(x['TITLE'])
            


# In[1]:


def chat():
    import pymongo
    from pymongo import MongoClient
    client=MongoClient('localhost',27017)
    client=MongoClient('mongodb://localhost:27017/')
    db=client['project_database']
    collection = db['project-collection']
    print("Start talking with the bot! (type 'quit' to stop, type 'help' to ask what it can do for you)/n")
    help_str="These are the types of questions I can answer for you: Top 5 movies or shows, latest/best movie or show, recommend movies and shows for different genres."
    print(help_str)
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break
        if inp.lower()=="help":
            print (help_str)
        result = model.predict([bag_of_words(inp, words)])[0]
        result_index = np.argmax(result)
        tag = labels[result_index]

        if result[result_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    give_response(tg["tag"])

        else:
            print("I didnt get that. Can you explain or try again from the options above.")
chat()


# In[ ]:




