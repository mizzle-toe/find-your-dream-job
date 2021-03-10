import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import joblib
from fydjob import utils
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
    data = data.drop(columns=['job_info_tokenized','job_text_tokenized_titlecase','job_text_tokenized'])

    #Sidebar
    # Title
    st.sidebar.markdown("""
        ### Please enter a job description in order to collect all relevant job offers and analyze the requirements
    """)

    # store Input in variable
    jd = st.sidebar.text_input('Job Description')
    #city = st.sidebar.text_input('City', 'Berlin')
    #comp = st.sidebar.text_input('Company')
    # use a regular expression for filtering the df, as Data Scientist (m/w/x) would be filtered out
    regex_jd = '^'+ jd
    #regex_city = '^'+ city
    #regex_comp = '^'+ comp
    #Button: if button is clicked, jump to next page and show exploratory view
    if st.sidebar.button('Analyze'):
        
        # filter data based on job input
        data = data.loc[data.job_title.str.contains(regex_jd)]  
        # filter data based on city input  only if we get the city
        #data = data.loc[data.location.str.contains(regex_city)]  
        # filter data based on job input
        #data = data.loc[data.job_title.str.contains(regex_comp)]
    

    # Numerical KPIs
    no_jd = str(data['job_id'].count())
    st.markdown("""
    ### Number of available jobs:""")
    st.write(no_jd)

    no_comp = str(data['company'].nunique())
    st.markdown("""
    ### Number of companies hiring:""")
    st.write(no_comp)


    # Altair Charts: breakdown by...
    #job description
    st.markdown("""
    ### Distribution of Search Terms:""")

    @st.cache(allow_output_mutation=True)
    def get_jobtitles():

        source_job = pd.DataFrame(data['query_text'].value_counts().reset_index())
        source_job= source_job.rename(columns = {'index':'Job', 'query_text':'Count'})
        
        c_jd= alt.Chart(source_job).mark_bar().encode(
        x='Count',
        y='Job'
        )
        text = c_jd.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Nudges text to right so it doesn't appear on top of the bar
        ).encode(
            text='Count:Q'
        )

        return c_jd+text

    c_jd = get_jobtitles()
    st.write(c_jd)

    #languages
    st.markdown("""
    ### Available jobs broken down by posting language:""")

    @st.cache(allow_output_mutation=True)
    def get_languages():
        source_lang = pd.DataFrame(data['tag_language'].value_counts()).reset_index()
        source_lang = source_lang.rename(columns = {'index':'Posting Language', 'tag_language':'Count'})
        c_language = alt.Chart(source_lang).transform_joinaggregate(
            Total='sum(Count)',
        ).transform_calculate(
            Percentage="datum.Count / datum.Total"
        ).mark_bar().encode(
            alt.X('Percentage:Q', axis=alt.Axis(format='.0%')),
            y='Posting Language:N'
        )
        return c_language
    c_lang = get_languages()
    st.write(c_lang)

    #companies
    st.markdown("""
    ### Top 30 available jobs by company:""")

    @st.cache(allow_output_mutation=True)
    def get_top_comp():
        #df
        source_comp = pd.DataFrame(data['company'].value_counts().reset_index())
        source_comp= source_comp.rename(columns = {'index':'Company', 'company':'Count'})
        source_comp = source_comp.nlargest(30, 'Count')
        #barchart
        bars = alt.Chart(source_comp).mark_bar().encode(
            x='Count:Q',
            y=alt.Y('Company:N', sort='-x')
        )
        # text on bars
        text = bars.mark_text(
            align='left',
            baseline='middle',
            dx=3  # Nudges text to right so it doesn't appear on top of the bar
        ).encode(
            text='Count:Q'
        )

        c_top_comp = (bars + text).properties(height=500)
        return c_top_comp
    #call companies
    c_top_comp = get_top_comp()
    st.write(c_top_comp)

    # most in demand skills from the dictionary
    st.markdown("""
    ### Most in demand skills:""")
    # skill count from utils:
    
    def get_skill_count():
        count = utils.count_skills(data['skills'])
        df_skills = pd.DataFrame()
        for key in count.keys():
            df_key=pd.DataFrame.from_dict(count[key])
            df_key['Category']=key
            df_skills = df_skills.append(df_key)
        source =df_skills.rename(columns = {0:'Skill',1:'Count'}).nlargest(50, columns='Count')
        #isolate the categories for the dropbox
        categs = np.array(df_skills['Category'].unique())
        category = np.insert(categs, 0, 'all')

        #Dropdownbox
        input_dropdown = alt.binding_select(options = category)
        selection = alt.selection_single(fields = ['Category'], bind = input_dropdown, name= 'Skill ')

        c_skills_count= alt.Chart(source).mark_bar().encode(
            x = ('Count:Q'),
            y = alt.Y('Skill',sort='-x')).add_selection(selection).transform_filter(selection)
        return c_skills_count
    c_skills_count = get_skill_count()
    st.write(c_skills_count)
