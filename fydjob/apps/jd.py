import streamlit as st
import altair as alt
import pandas as pd
import joblib
from fydjob import utils
from gensim.models.doc2vec import Doc2Vec
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
    #data = joblib.load('/Users/jasminkazi/code/mizzle-toe/find-your-dream-job/fydjob/output/indeed_proc/processed_data.joblib')
    data = data.drop(columns=['job_info_tokenized','job_text_tokenized_titlecase', 'job_title_tokenized','job_text_tokenized'])
    #data = data.head(100)

    #sidebar 

    # include text_area in case we decide a user can input JDs from other sites
    # jd = st.sidebar.text_area('Paste a job description to find similar job descriptions you could apply to','we might need a dummy description here')
    
    # extract the tokenized job description as it is used as input for the similar job offer search
    selected_index = st.sidebar.selectbox('Select job offer:', data.index)
    job_description = data.iloc[selected_index, [11]]
    #remove--> only used for testing and displaying which token has been selected
    #st.sidebar.write(job_description)
    #cols = data.columns
    #st.sidebar.write(cols)
    
    # list of job offers in detail
    #st.table(data)
    st.write(data)
    
    # load model to get similar offers based on the user selection
    model_loaded = Doc2Vec.load('/Users/jasminkazi/code/mizzle-toe/find-your-dream-job/fydjob/data/big_models/doc2vec_3000_15_epochs')
    infer_vector = model_loaded.infer_vector(job_description[0])
    similar_documents = model_loaded.docvecs.most_similar([infer_vector], topn = 5)
    #st.write(similar_documents)

    # filter data frame based on model output TODO: make the format pretty
    top_index = [text[0].replace('tag_', '') for text in similar_documents]
    similar_job_id = int(st.sidebar.radio('Select a similar job offer:', top_index))
    df_job = pd.DataFrame(data.loc[data['job_id'] == similar_job_id, ['job_id','job_title','job_text','company']])
    st.table(df_job)
    




