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



app = FastAPI()
home_path = os.path.dirname(fydjob.__file__)
df = NLPFrame().df


# define a root `/` endpoint
@app.get("/")
def data():
    'returns the entire dataframe'
    df_dict = df.to_dict()
    return df_dict

@app.get('/skills')
def skills(query,number):
    word_pipe = Word2VecPipeline(df)
    skill_list = word_pipe.most_similar_skills(query,int(number))
    tagged_skills = category_tagger(skill_list)

    return {"skills":tagged_skills}

@app.get('/jobs')
def jobs():
   doc_pipe = Doc2VecPipeline(df)



