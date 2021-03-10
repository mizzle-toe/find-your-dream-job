#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 15:57:26 2021

@author: vlud
"""
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

#GET A JOB
job = requests.get(API_URL + '/job', {'job_id': 1}).json()

#BIRD'S EYE VIEW
counts = requests.get(API_URL + '/counts').json()
search_terms = requests.get(API_URL + '/search_terms').json()
top_30 = requests.get(API_URL + '/top_companies').json()
skills_count = requests.get(API_URL + '/count_skills')

#SECOND PAGE
skills_match = requests.get(API_URL + '/skills', 
                            params = {'query': 'python'}).json()

#THIRD PAGE
job_match = requests.get(API_URL + '/jobs',
                         {'job_text': 'Hello world'}).json()