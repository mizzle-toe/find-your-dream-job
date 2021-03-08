#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 11:26:28 2021

@author: vlud

Structuring the entire data pipeline. 

1. IndeedScraper scrapes Indeed jobs and saves them as JSON. 

2. IndeedProcessor: 
    Loads JSON files and Kaggle dataset
    Removes duplicates with naive solution
    Assembles them into a single dataframe and exports it as joblib
    
3. Database loads the joblib, saves the jobs into database (if they are not there already).
   It can export the whole database as a dataframe. 
   
4. CleanDuplicates accesses the Database and removes duplicates according to 
   doc2vec solution. 

"""

from fydjob import IndeedProcessor, Database, NLPFrame

class Pipeline:
    
     def __init__(self):
         ...
         
     def long_pipeline(self):
         '''Performs the full pipeline (see readme).'''
         #Process Indeed scrapings and Kaggle data.
         ip = IndeedProcessor()
         ip.pipe()
         ip.export()
         
         #create and populate database
         db = Database()
         db.create_tables()
         db.populate(limit=None)
         
         #load dataframe from database 
         ndf = NLPFrame() 
         
         #similarity sweep
         ndf.get_duplicates()
         db.remove_sims_duplicates()
         ndf.reset_data()
         
         #add NLP fields
         ndf.add_token_fields()
         ndf.process_text()
         
     def short_pipeline(self):
        '''Short pipeline starting from database (see readme).'''
        ndf = NLPFrame()
        ndf.add_token_fields()
        ndf.process_text() 