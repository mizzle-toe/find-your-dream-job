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

@app.get('/jobs_title')
def jobs_title(job_ids):
    #job_ids = [int(x) for x in job_ids.split(',')]
    #job_ids = eval(job_ids
    job_ids = [int(x) for x in job_ids.split(',')]
    #return job_ids
    sel = df[['job_id', 'job_title']].set_index('job_id')
    present = [id_ for id_ in job_ids
               if id_ in sel.index]
    return sel.loc[job_ids].to_dict()['job_title']

@app.get('/counts')
def counts(query=None):
    if query:
        query_tokens = utils.tokenize_text(query)
        sel = df[df.job_title_tokenized.apply(lambda x: all([token in x for token in query_tokens]))]
    else:
        sel = df
    
    result = {'Number of avaialable jobs': len(sel),
              'Number of companies hiring': len(sel.company.unique())}
    return result

@app.get('/search_terms')
def search_terms(query):
    
    if query:
        query_tokens = utils.tokenize_text(query)
        sel = df[df.job_title_tokenized.apply(lambda x: all([token in x for token in query_tokens]))] 
    else:
        sel = df
    
    sel = sel.query_text[df.query_text != 'NULL']
    return (sel.value_counts(True) * 100).apply(lambda x: round(x)).to_dict()


@app.get('/top_companies')
def top_30(query=None, limit=30):
    if query:
        query_tokens = utils.tokenize_text(query)
        sel = df[df.job_title_tokenized.apply(lambda x: all([token in x for token in query_tokens]))]
    else:
        sel = df
    return sel.groupby('company').count().job_id.sort_values(ascending=False)[:limit].to_dict()

@app.get('/count_skills')
def top_skills(query):
    if query:
        query_tokens = utils.tokenize_text(query)
        sel = df[df.job_title_tokenized.apply(lambda x: all([token in x for token in query_tokens]))]
    else:
        sel = df
    return utils.count_skills(sel.skills)

@app.get('/skills')
def skills(query, number=5):
    skills_dict = utils.load_skills()
    
    all_skills = []
    for cat in skills_dict.keys():
        for word in skills_dict[cat]:
            all_skills.append(word)
    
    word_pipe = Word2VecPipeline(df)
    query_tokens=[token.strip() for token in query.lower().split(",")]
    query_tokens = [token for token in query_tokens if token]
    
    in_vocab = list(set([x for x in query_tokens if word_pipe.in_vocab(x)]))
    not_vocab = list(set([x for x in query_tokens if not word_pipe.in_vocab(x)]))
    
    skill_list = word_pipe.most_similar_skills(in_vocab, int(number))
    
    if not skill_list:
        return {'skills': None}
    tagged_skills = category_tagger(skill_list)
    return {"skills": tagged_skills,
            'found': in_vocab,
            'discarded': not_vocab}

@app.get('/jobs')
def jobs(job_text, limit=10):
   doc_pipe = Doc2VecPipeline()
   return doc_pipe.find_similar_jobs_from_string(job_text, number_offers=limit)

