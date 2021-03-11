#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import fydjob
import fydjob.utils as utils
import joblib
import multiprocessing
from fydjob.NLPFrame import NLPFrame

home_path = os.path.dirname(fydjob.__file__)

class Doc2VecPipeline:
    def __init__(self):
        print("Starting Doc2Vec...")
        self.folder = os.path.join(home_path, 'big_models')
        self.filepath = os.path.join(self.folder, 'doc2vec.joblib')
        self.texts_tagged_path = os.path.join(self.folder, 'texts_tagged.joblib')
        
        self.d2v_model = None
        self.df = NLPFrame().df
        
        #index df by job_id! 
        self.texts_tagged = self.load_texts_tagged(self.df)
                
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)            
        
        if os.path.exists(self.filepath):
            self.load_model()
        else:
            self.instantiate_model()
            self.save_model()
            
    def save_model(self):
        '''dd'''
        joblib.dump(self.d2v_model, self.filepath)
        print("Saving model in", self.filepath)
        
    def load_model(self):
        self.d2v_model = joblib.load(self.filepath)
        print("Loaded model from", self.filepath) 
        
    def load_texts_tagged(self, df, field='job_text_tokenized_processed'):
        '''Tag each text with correspondent job id.'''
        
        if os.path.exists(self.texts_tagged_path):
            print('Loading texts tagged...')
            return joblib.load(self.texts_tagged_path)
        else:
            sel = df[['job_id', field]]
            texts_tagged = [TaggedDocument(row[1], tags=[row[0]] ) for _, row in sel.iterrows()]
            joblib.dump(texts_tagged, self.texts_tagged_path)
            return texts_tagged
        
    def instantiate_model(self):
        '''instanciates model, using dbow (d=0)'''
        
        print("Instantiating doc2vec model...")
        
        cores = multiprocessing.cpu_count()
        self.d2v_model = Doc2Vec(documents=self.texts_tagged,
                         dm=0,
                         alpha=0.025,
                         vector_size=len(self.texts_tagged), 
                         min_count=1,
                         workers=cores,
                        )
        print(self.d2v_model)
        self.save_model()
        
    def train(self):
        ''' trains model'''
        print("Training doc2vec...")
        self.d2v_model.train(self.texts_tagged,
                             total_examples=self.d2v_model.corpus_count, 
                             epochs=15,
                         )
        self.save_model()
        print("Training complete") 
        
    def find_similar_jobs(self, tokenized_text, number_offers=10):
        ''' inputs: Doc2Vec model, string of a tokenized job offer, number of offers. 
        returns: tags of top x most similar job offers and similarity probabilities
        '''
        # infer vector from text 
        infer_vector = self.d2v_model.infer_vector(tokenized_text)
        # find similar offers
        similar_documents = self.d2v_model.docvecs.most_similar([infer_vector], topn = number_offers)
        return similar_documents
    
    def find_similar_jobs_from_string(self, string, number_offers=10):
        '''''' 
        tokenized_text = utils.tokenize_text_field(pd.Series(string)).iloc[0]
        tokenized_text = utils.lemmatize_words(tokenized_text)
        tokenized_text = utils.remove_stopwords_list(tokenized_text)
        
        return self.find_similar_jobs(tokenized_text, number_offers)
        
    