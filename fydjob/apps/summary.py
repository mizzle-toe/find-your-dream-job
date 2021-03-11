import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import joblib
from fydjob import utils
from fydjob.NLPFrame import NLPFrame
import requests
from fydjob.multiapp import MultiApp

API_URL = MultiApp().API_URL


def app():
    # get data from
    # api

    # BIRD'S EYE VIEW
    jd = st.sidebar.text_input('Job Description')
    
    search_terms = requests.get(API_URL + '/search_terms',
                                {'query': jd}).json()
    
    top_30 = requests.get(API_URL + '/top_companies', 
                          {'query': jd}).json()
    
    skills_count = requests.get(
        API_URL + '/count_skills', params={'limit': 10,
                                           'query': jd}).json()
    
    # store Input in variable
    
    counts = requests.get(API_URL + '/counts',
                          {'query': jd}).json()

    # local data
    #job = requests.get(API_URL + '/job', {'job_id': 1}).json()
    #data = NLPFrame().df
    #data = data.drop(columns=['job_info_tokenized','job_text_tokenized_titlecase','job_text_tokenized'])

    # Sidebar
    # Title
    st.sidebar.markdown("""
        ### Please enter a job description in order to collect all relevant job offers and analyze the requirements
    """)



    # use a regular expression for filtering the df, as Data Scientist (m/w/x) would be filtered out
    #regex_jd = '^'+ jd

    # Button: if button is clicked, jump to next page and show exploratory view
    # if st.sidebar.button('Analyze'):
    # filter data based on job input
    #data = data.loc[data.job_title.str.contains(regex_jd)]

    # Numerical KPIs
    #no_jd = str(data['job_id'].count())
    no_jd = str(counts['Number of avaialable jobs'])
    st.markdown("""
    ### Number of available jobs:""")
    st.write(no_jd)

    no_comp = str(counts['Number of companies hiring'])
    st.markdown("""
    ### Number of companies hiring:""")
    st.write(no_comp)

    # Altair Charts: breakdown by...
    # job description

    #@st.cache(allow_output_mutation=True)
    def get_jobtitles():

        source_job = pd.DataFrame(
            {'Categories': search_terms.keys(), 'Count': search_terms.values()})

        c_jd = alt.Chart(source_job).mark_bar().encode(
            x='Count',
            y='Categories'
        )
        text = c_jd.mark_text(
            align='left',
            baseline='middle',
            dx=3  # Nudges text to right so it doesn't appear on top of the bar
        ).encode(
            text='Count:Q'
        )

        return c_jd+text

    if search_terms:
        st.markdown('''### Distribution of Search Terms in Percent:''')
        c_jd = get_jobtitles()
        st.write(c_jd)

    # languages
   
    #@st.cache(allow_output_mutation=True)
    def get_languages():
        source_lang = pd.DataFrame(
            {"Language": ['German', 'English'], "Percentage": ['0.24', '0.76']})
        #source_lang = pd.DataFrame(data['tag_language'].value_counts()).reset_index()
        #source_lang = source_lang.rename(columns = {'index':'Posting Language', 'tag_language':'Count'})

        c_language = alt.Chart(source_lang).mark_bar().encode(
            alt.X('Percentage:Q', axis=alt.Axis(format='.0%')),
            y='Language'
        )
        # c_language = alt.Chart(source_lang).transform_joinaggregate(
        #     Total='sum(Count)',
        # ).transform_calculate(
        #     Percentage="datum.Count / datum.Total"
        # ).mark_bar().encode(
        #     alt.X('Percentage:Q', axis=alt.Axis(format='.0%')),
        #     y='Posting Language:N'
        # )
        return c_language
    
    if not jd:
        st.markdown('''### Available jobs broken down by posting language in percent:''')
        c_lang = get_languages()
        st.write(c_lang)

    # companies
    st.markdown("""
    ### Top 30 available jobs by company:""")

    #@st.cache(allow_output_mutation=True)
    def get_top_comp():
        # df
        source_comp = pd.DataFrame(
            {'Company': top_30.keys(), 'Count': top_30.values()})
        # barchart
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

        c_top_comp = (bars + text)
        return c_top_comp
    # call companies
    c_top_comp = get_top_comp()
    st.write(c_top_comp)

    # most in demand skills from the dictionary
    st.markdown("""
    ### Most in demand skills:""")
    # skill count from utils:

    def get_skill_count():
        counts = []

        for key, val in skills_count.items():
            for t in val:
                counts.append([t[0], t[1], key])
        source = pd.DataFrame(counts, columns=['Skill', 'Count', 'Category']).sort_values(
            'Count', ascending=False).nlargest(50, columns='Count')

        # isolate the categories for the dropbox
        categs = np.array(source['Category'].unique())
        category = np.insert(categs, 0, 'all')

        # Dropdownbox
        input_dropdown = alt.binding_select(options=category)
        selection = alt.selection_single(
            fields=['Category'], bind=input_dropdown, name='Skill ')

        c_skills_count = alt.Chart(source).mark_bar().encode(
            x=('Count:Q'),
            y=alt.Y('Skill', sort='-x')).add_selection(selection).transform_filter(selection)
        return c_skills_count
    c_skills_count = get_skill_count()
    st.write(c_skills_count)
