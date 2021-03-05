#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 12:56:56 2021

@author: vlud
"""
import os
import fydjob
from fydjob.Database import Database
import fydjob.utils as utils
import joblib

home_path = os.path.dirname(fydjob.__file__)

class NLPFrame:
    def __init__(self):
        self.joblib_path = os.path.join(home_path, 'output', 'nlp_frame.joblib')
        self.db = Database()
         self.df = db.to_frame()
         print('Loaded dataframe.') 
         
    def load_from_db(self):
        df = self.db.to_frame()
        return df
    
    def load_from_joblib(self, path):
        
        return 
    
    def add_token_fields(self):
        '''Adds columns with tokens.'''
        self.df['job_info_tokenized'] = utils.tokenize_text_field(self.df['job_info'])
        self.df['job_text_tokenized'] = utils.tokenize_text_field(self.df['job_text'])
        self.df['job_text_tokenized_titlecase'] = utils.tokenize_text_field(self.df['job_info'], to_lowercase=False)
        self.df['job_title_tokenized'] = utils.tokenize_text_field(self.df['job_title'])
        
    def process_text(self, text_field='job_text_tokenized'):
        '''Applies further processing to the text field.'''
        
        new_col = self.df[text_field].apply(utils.join_strings)\
                                     .apply(utils.lemmatize_words)\
                                     .apply(utils.remove_stopwords)
                                     
        self.df[text_field + "_processed"] = new_col
        

df = NLPFrame()
df.add_token_fields()
df.process_text()