#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 10:47:16 2021

@author: vlud
"""

from fastapi import FastAPI
from fydjob.Word2VecPipeline import Word2VecPipeline
from fydjob.utils import category_tagger
from fydjob.NLPFrame import NLPFrame
from fydjob.Doc2VecPipeline import Doc2VecPipeline
import os
import fydjob
import fydjob.utils as utils

app = FastAPI()
home_path = os.path.dirname(fydjob.__file__)
df = NLPFrame().df

# define a root `/` endpoint
@app.get("/")
def data():
    'returns the entire dataframe'
    #df_dict = df.to_dict()
    #return df_dict
    
@app.get('/job')
def job(job_id):
    return df.set_index('job_id').loc[int(job_id)].to_dict()

@app.get('/counts')
def counts():
    result = {'Number of avaialable jobs': len(df),
              'Number of companies hiring': len(df.company.unique())}
    return result

@app.get('/search_terms')
def search_terms():
    sel = df.query_text[df.query_text != 'NULL']
    return (sel.value_counts(True) * 100).apply(lambda x: round(x,2)).to_dict()


@app.get('/top_companies')
def top_30(limit=30):
    return df.groupby('company').count().job_id.sort_values(ascending=False)[:limit].to_dict()

@app.get('/count_skills')
def top_skills():
    return utils.count_skills(df.skills)


@app.get('/skills')
def skills(query,number=5):
    word_pipe = Word2VecPipeline(df)
    skill_list = word_pipe.most_similar_skills(query,int(number))
    tagged_skills = category_tagger(skill_list)

    return {"skills":tagged_skills}

@app.get('/jobs')
def jobs(job_text, limit=10):
   doc_pipe = Doc2VecPipeline()
   return doc_pipe.find_similar_jobs_from_string(job_text, number_offers=limit)

