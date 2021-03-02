import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# get data, use URL later instead
data = pd.read_json('/Users/jasminkazi/code/mizzle-toe/find-your-dream-job/raw_data/glassdoor_scraper_output/data_scientist_in_berlin_2020-09-03.json')


# Title
st.sidebar.markdown("""
    # Find your Dream Job
    ## Please enter the following in order to collect all relevant job offers and analyze the requirements 
""")

# store Input in variable
jd = st.sidebar.text_input('Job Description', 'Data Scientist')
# use a regular expression for filtering the df, as Data Scientist (m/w/x) would be filtered out
regex_jd = '^'+jd
city = st.sidebar.text_input('City', 'Berlin')
comp = st.sidebar.text_input('Company')

#Button: if button is clicked, jump to next page and show exploratory view
if st.sidebar.button('Analyze'):
    # filter data based on job input
    data = data.loc[data.position.str.contains(regex_jd)]
    # filter data based on city input  only if we get the city

# switch between pages by using Radio Button
st.radio('Radio', [1,2,3])

# Numerical KPI
no_jd = str(data['position'].count())
st.markdown("""
### Number of available jobs:""")
st.write(no_jd)

no_comp = str(data['company'].nunique())
st.markdown("""
### Number of companies hiring:""")
st.write(no_comp)

# Chart

st.markdown("""
### Top 30 available jobs by company:""")
#altair
@st.cache
def get_top_30():
    data_comp = data.groupby(data['company']).count().reset_index()
    top_30= data_comp.nlargest(30, 'position').drop(columns=['description', 'url'])
    c_top_30= alt.Chart(top_30).mark_bar().encode(
        x='position:Q',
        y=alt.Y('company:N', sort='-x')
    )
    return c_top_30


c_top_30 = get_top_30()
st.write(c_top_30)

#table
st.table(data)

