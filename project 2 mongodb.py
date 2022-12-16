#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Imports
import pandas as pd
import pymongo
from pymongo import MongoClient



# Load csv dataset
data = pd.read_csv('<<INSERT NAME OF DATASET>>.csv')

# Connect to MongoDB
client=MongoClient('localhost',27017)
client=MongoClient('mongodb://localhost:27017/')
db=client.test_database
db=client['test_database']
collection = db.test_collection
collection = db['test-collection']

client =  MongoClient("mongodb+srv://<<YOUR USERNAME>>:<<PASSWORD>>@clustertest-icsum.mongodb.net/test?retryWrites=true&w=majority")
db = client['<<INSERT NAME OF DATABASE>>']
collection = db['<<INSERT NAME OF COLLECTION>>']
data.reset_index(inplace=True)
data_dict = data.to_dict("records")

# Insert collection
collection.insert_many(data_dict)

