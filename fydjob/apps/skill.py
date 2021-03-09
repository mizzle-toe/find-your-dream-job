import streamlit as st
import altair as alt
import pandas as pd
from gensim.models import Word2Vec
from fydjob.Word2VecPipeline import WordPipeline


def app():
    #sidebar 
    skill = st.sidebar.text_input('Search skill','python')
    word = [skill]
    #add number of skills and pass new model from alex!!!
    no_skill = st.sidebar.number_input('n-closest skills',10)
    
    #search for skill
    st.markdown("""
    ### Find the closest skills for:""")
    st.write(skill)

    # Model
    # replace with API
    
    # old model
    w2v_model = Word2Vec.load("/Users/jasminkazi/code/mizzle-toe/find-your-dream-job/fydjob/data/models/w2v_model_baseline.model")
    df_words= pd.DataFrame(w2v_model.wv.most_similar(word), columns=['Similar word', 'distance']).assign(hack='').set_index('hack') # works with single words
    
    #new model with n-recommendation
    #w2v_model = WordPipeline("/Users/jasminkazi/code/mizzle-toe/find-your-dream-job/fydjob/data/models/w2v_model_baseline.model")
    #df_words= pd.DataFrame(w2v_model.most_similar_skills(skill,n_recommendations= no_skill)).assign(hack='').set_index('hack')
    
    #table
    st.write(df_words)
  

