#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 08:52:21 2021

@author: vlud
"""
import pymongo
import fydjob
from fydjob.NLPFrame import NLPFrame

ndf = NLPFrame().df

client = pymongo.MongoClient("mongodb+srv://vlad-ds:<password>@cluster0.7akd3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.test

