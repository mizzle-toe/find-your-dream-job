import streamlit as st
import altair as alt
import pandas as pd
from fydjob.Word2VecPipeline import Word2VecPipeline
from fydjob.utils import category_tagger
from fydjob.NLPFrame import NLPFrame
import requests

from fydjob.multiapp import MultiApp
API_URL = MultiApp().API_URL

def app():
    # User input
    skills = st.sidebar.text_input('Search skill/s','python')
    no_skill = st.sidebar.number_input('number of closest skills',5)

    #API call
    skills_match = requests.get(API_URL + '/skills', 
                            params = {'query': skills.strip(), 
                                      'number': no_skill}).json()
    
    #model with n-recommendation
    lol = skills_match['skills']
       
    if lol:
        found = skills_match['found']
        discarded = skills_match['discarded']
         
        df_words = pd.DataFrame({'Skill': [x[0].title() for x in lol], 'Category': [x[1].title() for x in lol]}).assign(hack='').set_index('hack')
        
        st.markdown('''### Find the most similar skills for:''')
        st.write(', '.join(found))
        
        if discarded:
            st.markdown('''### Sorry, we couldn't find:''')
            st.write(', '.join(discarded))

        #table
        st.write(df_words)
        
    else:
        st.write("Sorry, no result.")