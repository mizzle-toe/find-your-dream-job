#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 12:56:56 2021

@author: vlud

TODO: Add feature with skills list & code keywords search

"""
import os
import fydjob
from fydjob.Database import Database
import fydjob.utils as utils
import joblib
import nltk

home_path = os.path.dirname(fydjob.__file__)

class NLPFrame:
    def __init__(self):
        self.nltk_downloads()
        self.joblib_path = os.path.join(home_path, 'output', 'nlp_frame.joblib')
        self.df = None
        self.load_data() 
        
    def nltk_downloads(self):
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('stopwords')
            
    def load_data(self):
        '''Loads data from joblib file, and if absent loads it from database
        and creates the joblib file.
        '''
        if os.path.exists(self.joblib_path):
            self._load_from_joblib() 
        else:
            self._load_from_db()
        
    def _load_from_db(self):
        db = Database()
        self.df = db.to_frame()
        self.save_joblib()
        print("Loaded from db.")
    
    def _load_from_joblib(self):
        self.df = joblib.load(self.joblib_path)
        print("Loaded from", self.joblib_path)
    
    def save_joblib(self):
        joblib.dump(self.df, self.joblib_path)
        print(f"Saved at {self.joblib_path}")
        
    def reset_data(self):
        '''Removes the joblib file and reloads the data.'''
        os.remove(self.joblib_path)
        self.load_data()

    def add_token_fields(self, force=False):
        '''Adds columns with tokens.'''
        
        cols = ['job_info_tokenized', 'job_text_tokenized',
                'job_text_tokenized_titlecase', 'job_title_tokenized']
        
        if force or not all([col in self.df.columns for col in cols]):
            print("Tokenizing text fields...")
            self.df['job_info_tokenized'] = utils.tokenize_text_field(self.df['job_info'])
            self.df['job_text_tokenized'] = utils.tokenize_text_field(self.df['job_text'])
            self.df['job_text_tokenized_titlecase'] = utils.tokenize_text_field(self.df['job_info'], to_lowercase=False)
            self.df['job_title_tokenized'] = utils.tokenize_text_field(self.df['job_title'])
            self.save_joblib()
        else:
            print('Token columns already found.')
        
    def process_text(self, text_field='job_text_tokenized', force=False):
        '''Applies further processing to the text field.'''
        
        colname = text_field + "_processed"
        
        if force or colname not in self.df.columns:
            print("Processing", text_field)
            self.df[colname] = self.df[text_field].apply(utils.lemmatize_words)\
                                                  .apply(utils.remove_stopwords_list)
            self.save_joblib()
        else:
            print("Processed column already found.")
            
    def get_duplicates(self, field='job_text_tokenized', threshold=.95):
        '''Identifies duplicates according to the 'shared unique tokens' similarity score.
        Returns a list of job ids that can be passed to the database for deletion.
        TODO: Exclude Kaggle. 
        ''' 
        print('Extracting duplicates list with similarity measure.')
        
        indexes_to_remove_path = os.path.join(home_path, 'output', 'duplicates_indexes.joblib')
        
        if not os.path.exists(indexes_to_remove_path):
            joblib.dump([], indexes_to_remove_path)
        
        indexes_to_remove = joblib.load(indexes_to_remove_path)
        
        col = self.df[field]
        df = self.df.copy()
        
        c = 50
        
        for index, row in df.iterrows():
            c -= 1
            
            if not c:
                print('Saving indexes...')
                joblib.dump(indexes_to_remove, indexes_to_remove_path)
                c = 50
            
            if index not in indexes_to_remove:
                text = row[field]
                sims = utils.get_similarities(text, col)
                indexes = [sim[0] for sim in sims
                           if sim[0] != index
                           and sim[1] >= threshold] 
                indexes_to_remove += indexes
                #prevent duplicates
                indexes_to_remove = list(set(indexes_to_remove))
                print(index, indexes)
                
        job_ids_to_remove = list(df.loc[indexes_to_remove]['job_id'])
        
        #exporting
        sdi_path = os.path.join(home_path, 'output', 'sims_duplicates_ids.joblib') 
        joblib.dump(job_ids_to_remove, sdi_path)
        print("Saved duplicate IDs at", sdi_path)
        
            
ndf = NLPFrame() 
#ndf.add_token_fields()
#ndf.process_text()
#job_ids_to_drop = ndf.get_duplicates()
#joblib.drop(job_ids_to_drop, 'output/job_ids_to_drop.joblib')
#ndf.add_token_fields()
#ndf.process_text()
