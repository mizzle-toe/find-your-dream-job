import streamlit as st
import altair as alt
import pandas as pd
import joblib
from fydjob import utils
from fydjob.Doc2VecPipeline import Doc2VecPipeline
from fydjob.NLPFrame import NLPFrame
import requests

def app():
    # model for similar offers based on text input
    jd = st.text_area('Paste a job description you like and find similar job descriptions you could apply to','google')
    
    # get data from
    #api
    API_URL = "http://0.0.0.0:3000"
    job_match = requests.get(API_URL + '/jobs',
                         {'job_text': jd}).json()
    job_match = sorted(job_match, key= lambda x: x[1])

    #local data
    #data = NLPFrame().df
    #data = data.drop(columns=['job_info_tokenized','job_text_tokenized_titlecase', 'job_title_tokenized','job_text_tokenized'])
    #data = data.head(5800)

    ##sidebar 

    # filter data frame based on model output 

    #model = Doc2VecPipeline()
    #similar_documents = model.find_similar_jobs_from_string(jd)
    similar_documents = [int(x[0].split('_')[-1]) for x in job_match]
    #top_index = [text[0].replace('job_id_', '') for text in similar_documents]
    similar_job_id = int(st.sidebar.radio('Select a similar job offer:', similar_documents))


    #TODO for later: instead of printig the job tag we could print the beginning of the job text followed by ...
    #similar_job_text = data.loc[data['job_id'] == top_index, ['job_text']]
    #similar_job_id = int(st.sidebar.radio('Select a similar job offer:', similar_job_text))
    
    #formatting of the similar JD
    job = requests.get(API_URL + '/job', {'job_id': similar_job_id}).json()
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




