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
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

home_path = os.path.dirname(fydjob.__file__)

class NLPFrame:
    def __init__(self):
        self.joblib_path = os.path.join(home_path, 'output', 'nlp_frame.joblib')
        
        self.dbow_path = os.path.join(home_path, 'output', 'models', 'model_dbow.joblib')
        #self.dbow = self.load_dbow()
        
        if os.path.exists(self.joblib_path):
            self.df = joblib.load(self.joblib_path)
            print("Loaded from", self.joblib_path)
        else:
            self.df = self.load_from_db()
            print("Loaded from db.")
            self.save_joblib()
        
    def load_from_db(self):
        db = Database()
        return db.to_frame()
    
    def load_dbow(self):
        if os.path.exists(self.dbow_path):
            return joblib.load(self.dbow_path)
        return
    
    def save_joblib(self):
        joblib.dump(self.df, self.joblib_path)
        print(f"Saved at {self.joblib_path}")

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
                                                  .apply(utils.remove_stopwords)
            self.save_joblib()
        else:
            print("Processed column already found.")
            
    def get_duplicates(self, field='job_text_tokenized', threshold=.95):
        '''Identifies duplicates according to the 'shared unique tokens' similarity score.
        Returns a list of job ids that can be passed to the database for deletion.
        TODO: Exclude Kaggle. 
        '''
        indexes_to_remove = []
        col = self.df[field]
        df = self.df.copy()
        df = df.reset_index()
        
        for index, row in df.iterrows():
            if index not in indexes_to_remove:
                text = row[field]
                sims = utils.get_similarities(text, col)
                indexes = [sim[0] for sim in sims
                           if sim[0] != index
                           and sim[1] >= threshold] 
                indexes_to_remove += indexes
                print(index, indexes)
                
        job_ids_to_remove = list(df.loc[indexes_to_remove]['job_id'])
        return job_ids_to_remove
        
            
    def train_dbow(self, field='job_text_tokenized_processed'):
        '''Trains the model for doc2vec similarity.'''
        print("Training dbow model...")
        texts = self.df[field]
        texts_tagged = [TaggedDocument(text, tags=['tag_'+str(tag)]) for tag, text in enumerate(texts)]
        
        # build vocabulary with CBOW (dm=0) - instanciate model
        model_dbow = Doc2Vec(documents=texts_tagged,
                     dm=0,
                     alpha=0.025,
                     vector_size=len(texts_tagged), 
                     min_count=1)
        
        # train the model
        model_dbow.train(texts_tagged, total_examples=model_dbow.corpus_count, epochs=1)
        joblib.dump(model_dbow, self.dbow_path)
        print(f"Saved model at {self.dbow_path}")
        self.load_dbow()
        
    def find_similar_jobs(self, tokenized_job):
        # infer vector from text
        infer_vector = self.dbow.infer_vector(tokenized_job)
        # finds similar texts
        similar_documents = self.dbow.docvecs.most_similar([infer_vector], topn = 30)
        return similar_documents
        
ndf = NLPFrame()
#job_ids_to_drop = ndf.get_duplicates()
#joblib.drop(job_ids_to_drop, 'output/job_ids_to_drop.joblib')


#ndf.add_token_fields()
#ndf.process_text()
