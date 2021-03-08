#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 10:47:16 2021

@author: vlud
"""

from fastapi import FastAPI

app = FastAPI()

# define a root `/` endpoint
@app.get("/")
def index():
    return {"ok": True}

@app.get('/skills')
def skills():
    return {'skills': ['python', 'java', 'docker']}