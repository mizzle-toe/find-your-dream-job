#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import os
import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import fydjob
import joblib
import multiprocessing

home_path = os.path.dirname(fydjob.__file__)

class DocPipeline:
    def __init__(self, df):
        
        self.folder = os.path.join(home_path, 'big_models')
        self.filepath = os.path.join(self.folder, 'doc2vec.joblib')
        self.texts_tagged_path = os.path.join(self.folder, 'texts_tagged.joblib')
        
        self.d2v_model = None
        self.df = df
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
            series = pd.Series(list(df[field]), index=df['job_id'])
            texts_tagged = [TaggedDocument(text, tags=['job_id_'+str(tag)]) for tag, text in enumerate(series)]
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


from fydjob.NLPFrame import NLPFrame
df = NLPFrame().df
dp = DocPipeline(df)
dp.train()
