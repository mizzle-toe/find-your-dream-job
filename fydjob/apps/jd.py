import os
import streamlit as st
import altair as alt
import pandas as pd
import joblib
from fydjob import utils
from fydjob.Doc2VecPipeline import Doc2VecPipeline
from fydjob.NLPFrame import NLPFrame
import requests
import json

from fydjob.multiapp import MultiApp
API_URL = MultiApp().API_URL

def radio(similar_jobs, docs_list):
    if docs_list:
        selection = st.sidebar.radio('Select a similar job offer:', docs_list)
        similar_job_id = int(selection.split('|')[0].strip())
        job = similar_jobs[similar_job_id]
        sim_jd = job['job_text']
        sim_title = job['job_title']
        sim_comp = job['company']
        sim_skills = sorted(list(set([x[0] for x in job['skills']])))
        job_link = job['job_link']
        
        st.markdown("""
            ## Find the details for the selected similar job offer below
            ### Job Title:
        """)
        st.write(sim_title)
        st.markdown("""
            ### Company:
        """)
        st.write(sim_comp)
        st.markdown("""
            ### Required skills:
        """)
        skills_string = ', '.join(sim_skills) 
        
        st.write(skills_string)
        st.markdown("""
            ### Job Description:
        """)
        st.write(sim_jd)
    
        if job_link != 'NULL':
            st.write('Apply here', job_link)    
        

def app():
    # model for similar offers based on text input
    jd = st.text_area('Paste a job description you like and find similar job descriptions you could apply to','google')
    docs_list = []
    job_match = None
    
    if st.button('Analyze'):
       
        try:
            os.remove('cache.joblib')
        except:
            pass
        
        # get data from
        #api
        job_match = requests.get(API_URL + '/jobs',
                             {'job_text': jd}).json()
        job_match = sorted(job_match, key= lambda x: x[1])

        
        similar_documents = [int(x[0].split('_')[-1]) for x in job_match]
        ids_str = ','.join([str(x) for x in similar_documents])
        jobs = requests.get(API_URL + '/jobs_title', params={'job_ids': ','.join([str(x) for x in similar_documents])}).json()
        char_limit = 50
        for job_id, title in jobs.items():
            tag = str(job_id)
            if title:
                tag += ' | ' + title[:20] + '...' if len(title) > 20 else ''
            docs_list.append(tag)
        
        similar_jobs = {}
        
        for job_id in similar_documents:
            job = requests.get(API_URL + '/job', {'job_id': job_id}).json()
            similar_jobs[job_id] = job
            
        to_cache = {'similar_jobs': similar_jobs,
                    'docs_list': docs_list}
        
        joblib.dump(to_cache, 'cache.joblib')
        
        radio(similar_jobs, docs_list)
            
    try:
        cache = joblib.load('cache.joblib')
    except:
        cache = None
        
    if cache:
        radio(cache['similar_jobs'], cache['docs_list'])
    

    
    
    
    
    
