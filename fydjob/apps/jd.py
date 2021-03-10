import streamlit as st
import altair as alt
import pandas as pd
import joblib
from fydjob import utils
from fydjob.Doc2VecPipeline import Doc2VecPipeline
from fydjob.NLPFrame import NLPFrame
import requests

def app():
    # get data from
    #api
    #url = 'http://0.0.0.0:3000'
    #response = requests.get(url)
    #response.json()

    #local data
    data = NLPFrame().df
    data = data.drop(columns=['job_info_tokenized','job_text_tokenized_titlecase', 'job_title_tokenized','job_text_tokenized'])
    data = data.head(5800)

    ##sidebar 
    ## extract the tokenized job description as it is used as input for the similar job offer search
    #selected_index = st.sidebar.selectbox('Select Job ID:', data.job_id)
    #job_description = data.iloc[selected_index, [11]]

    ## list of job offers in detail
    #source_df = data[['job_id','skills']]
    #st.write(source_df.assign(hack='').set_index('hack'))
    
    ## model to get similar offers based on the job id selection
    # model_loaded = Doc2Vec.load('/Users/jasminkazi/code/mizzle-toe/find-your-dream-job/fydjob/data/big_models/doc2vec_3000_15_epochs')
    # infer_vector = model_loaded.infer_vector(job_description[0])
    # similar_documents = model_loaded.docvecs.most_similar([infer_vector], topn = 5)
    # top_index = [text[0].replace('tag_', '') for text in similar_documents]
    # similar_job_id = int(st.sidebar.radio('Select a similar job offer:', top_index))
    # st.write(similar_documents)

    # model for similar offers based on text input
    jd = st.text_area('Paste a job description you like and find similar job descriptions you could apply to','we might need a dummy description here')

    # filter data frame based on model output 
    model = Doc2VecPipeline()
    similar_documents = model.find_similar_jobs_from_string(jd)
    top_index = [text[0].replace('job_id_', '') for text in similar_documents]
    similar_job_id = int(st.sidebar.radio('Select a similar job offer:', top_index))


    #TODO for later: instead of printig the job tag we could print the beginning of the job text followed by ...
    #similar_job_text = data.loc[data['job_id'] == top_index, ['job_text']]
    #similar_job_id = int(st.sidebar.radio('Select a similar job offer:', similar_job_text))
    
    #formatting of the similar JD
    cur_ind = data.set_index('job_id').loc[similar_job_id]
    sim_jd = cur_ind['job_text']
    sim_title = cur_ind['job_title']
    sim_comp = cur_ind['company']
    sim_skills = cur_ind['skills']
    job_link = cur_ind['job_link']
    #sim_title = data.loc[data['job_id'] == similar_job_id, ['job_title']].iloc[0,0]
    #sim_comp = data.loc[data['job_id'] == similar_job_id, ['company']].iloc[0,0]
    #sim_skills = data.loc[data['job_id'] == similar_job_id, ['skills']].iloc[0,0]
    #sim_jd = data.loc[data['job_id'] == similar_job_id, ['job_text']].iloc[0,0]
    #job_link = data.loc[data['job_id'] == similar_job_id, ['job_link']].iloc[0,0]
    #skill_list = []
    for skill in sim_skills:
        st.write(skill[0])
        #skill_list=skill_list.append(skill[0])


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
        ### Rewuired skills:
    """)
    #st.write(skill_list)
    st.markdown("""
        ### Job Description:
    """)
    st.write(sim_jd)

    if job_link != 'NULL':
        st.write('Apply here', job_link)    




