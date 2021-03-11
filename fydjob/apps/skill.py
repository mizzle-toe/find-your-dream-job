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
      #sidebar 
    skills = st.sidebar.text_input('Search skill','python')
    skills = skills.strip()
    #word = [skills.split(',')]
    no_skill = st.sidebar.number_input('n-closest skills',5)

    API_URL = "http://0.0.0.0:3000"
    skills_match = requests.get(API_URL + '/skills', 
                            params = {'query': skills, 'number': no_skill}).json()
    
    #search for skill
    st.markdown("""
    ### Find the closest skills for:""")
    st.write(skills)
    
    #model with n-recommendation
    lol = skills_match['skills']

    df_words = pd.DataFrame({'Skill': [x[0].title() for x in lol], 'Category': [x[1].title() for x in lol]}).assign(hack='').set_index('hack')
    
    #table
    st.write(df_words)
  

