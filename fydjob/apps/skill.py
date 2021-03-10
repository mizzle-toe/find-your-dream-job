import streamlit as st
import altair as alt
import pandas as pd
from fydjob.Word2VecPipeline import Word2VecPipeline
from fydjob.utils import category_tagger
from fydjob.NLPFrame import NLPFrame
import requests


def app():
    # Model
    # get data from
    #api
    #url = 'http://0.0.0.0:3000'
    #response = requests.get(url)
    #response.json()

    #sidebar 
    skills = st.sidebar.text_input('Search skill','python')
    skills = skills.strip()
    #word = [skills.split(',')]
    no_skill = st.sidebar.number_input('n-closest skills',5)
    
    #search for skill
    st.markdown("""
    ### Find the closest skills for:""")
    st.write(skills)
    
    #model with n-recommendation
    w2v_model = Word2VecPipeline()
    df_words = pd.DataFrame(category_tagger(w2v_model.most_similar_skills(skills,n_recommendations= no_skill)),columns=['List of similar words','Skill category']).assign(hack='').set_index('hack')

    #table
    st.write(df_words)
  

