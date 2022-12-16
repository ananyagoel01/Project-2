#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Imports
import pandas as pd
import pymongo
from pymongo import MongoClient



# Load csv dataset
movie_data = pd.read_csv('/Users/ananyagoel/Desktop/DS 2002/Best Movie by Year Netflix.csv')


# In[3]:


movie_data.columns


# In[4]:


movie_data=movie_data[['TITLE', 'RELEASE_YEAR', 'SCORE', 'MAIN_GENRE']]


# In[5]:


movie_data["TYPE"]=movie_data["TITLE"].apply(lambda x:"movie")


# In[6]:


movie_data.head()


# In[7]:


shows_data = pd.read_csv('/Users/ananyagoel/Desktop/DS 2002/Best Show by Year Netflix.csv')


# In[8]:


shows_data=shows_data[['TITLE', 'RELEASE_YEAR', 'SCORE', 'MAIN_GENRE']]


# In[9]:


shows_data["TYPE"]=shows_data["TITLE"].apply(lambda x:"show")


# In[10]:


shows_data.head()


# In[11]:


data=pd.concat([movie_data,shows_data],ignore_index=True)


# In[12]:



# Connect to MongoDB
client=MongoClient('localhost',27017)
client=MongoClient('mongodb://localhost:27017/')
db=client.project_database
db=client['project_database']
collection = db.project_collection
collection = db['project-collection']


data_dict = data.to_dict("records")

# Insert collection
collection.insert_many(data_dict)


# In[13]:


db.list_collection_names()

