import streamlit as st
import altair as alt
import pandas as pd
import joblib
from fydjob import utils
from gensim.models import Word2Vec

#Detail page
w2v_model = Word2Vec.load("../fydjob/data/models/w2v_model_baseline.model")
#search for skill
st.markdown("""
### Find the closest skills for:""")
skill = st.text_input('Skill','python')
word = [skill]
#st.write(skill)
df_words= pd.DataFrame(w2v_model.wv.most_similar(word), columns=['Similar word', 'distance']) # works with single words
#table
st.table(df_words)


