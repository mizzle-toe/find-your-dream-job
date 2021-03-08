import streamlit as st
import altair as alt
import pandas as pd
import joblib
from fydjob import utils
from gensim.models import Word2Vec

def app():
    #sidebar 
    skill = st.sidebar.text_input('Search skill','python')
    word = [skill]
    #add number of skills and pass new model from alex!!!
    no_skill = st.sidebar.number_input('n-closest skills',10)

    #Model
    w2v_model = Word2Vec.load("../fydjob/data/models/w2v_model_baseline.model")
    #search for skill
    st.markdown("""
    ### Find the closest skills for:""")
    st.write(skill)
    df_words= pd.DataFrame(w2v_model.wv.most_similar(word), columns=['Similar word', 'distance']).assign(hack='').set_index('hack') # works with single words
    #table
    st.write(df_words)
  

