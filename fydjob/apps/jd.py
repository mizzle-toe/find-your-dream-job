import streamlit as st
import altair as alt
import pandas as pd
import joblib
from fydjob import utils
from gensim.models.doc2vec import Doc2Vec

def app():
        # get data --> replace by api call!
    data = joblib.load('/Users/jasminkazi/code/mizzle-toe/find-your-dream-job/fydjob/output/indeed_proc/processed_data.joblib')
    data = data.drop(columns=['job_info_tokenized','job_text_tokenized_titlecase', 'job_title_tokenized'])
    data = data.head(100)

    #sidebar 

    # include text_are in case we decide a user can input JDs from other sites
    # jd = st.sidebar.text_area('Paste a job description to find similar job descriptions you could apply to','we might need a dummy description here')
    
    # extract the tokenized job description as it is used as input for the similar job offer search
    selected_index = st.sidebar.selectbox('Select job offer:', data.index)
    job_description = data.iloc[selected_index, [10]]
    #remove--> only used for testing and displaying which token has been selected
    st.sidebar.write(job_description)
    cols = data.columns
    st.sidebar.write(cols)
    
    # list of job offers in detail
    #st.table(data)
    st.write(data)
    
    # load model to get similar offers based on the user selection
    model_loaded = Doc2Vec.load('/Users/jasminkazi/code/mizzle-toe/find-your-dream-job/fydjob/data/big_models/doc2vec_3000_15_epochs')
    infer_vector = model_loaded.infer_vector(job_description[0])
    similar_documents = model_loaded.docvecs.most_similar([infer_vector], topn = 5)
    st.write(similar_documents)

    #filter data frame based on model output
    #top_index = [text[0].replace('tag_', '') for text in similar_documents]
    #top_offers = pd.DataFrame(data.iloc[top_index]['job_text'])
    #top_offers['similarities'] = [text[1] for text in similar_documents]
    #st.write(top_offers)
    




