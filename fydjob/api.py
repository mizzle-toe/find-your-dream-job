#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 10:47:16 2021

@author: vlud
"""

from fastapi import FastAPI
from fydjob.Word2VecPipeline import WordPipeline
from fydjob.utils import category_tagger
from fydjob.NLPFrame import NLPFrame
import os
import fydjob



app = FastAPI()
home_path = os.path.dirname(fydjob.__file__)
model_path = os.path.join(home_path, 'data', 'models', 'w2v_model_baseline.model')


# define a root `/` endpoint
@app.get("/")
def data():
    df = NLPFrame().df
    df_dict = df.head(5).to_dict()
    return df_dict

@app.get('/skills')
def skills(query):
    pipeline = WordPipeline(model_path)
    skill_list = pipeline.most_similar_skills(query,n_recommendations= 10)
    tagged_skills = category_tagger(skill_list)

    return {'skills': tagged_skills}

