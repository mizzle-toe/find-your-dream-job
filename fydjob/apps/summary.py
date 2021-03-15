import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
from fydjob.multiapp import MultiApp
import requests


API_URL = MultiApp().API_URL


def app():
    
    # Title and user input
    st.sidebar.markdown(''' #### Please enter a job description in order to collect all relevant job offers and analyze the requirements''')
    jd = st.sidebar.text_input('Job Description')
    
    #API calls
    search_terms = requests.get(API_URL + '/search_terms',
                                {'query': jd}).json()
    
    top_30 = requests.get(API_URL + '/top_companies', 
                          {'query': jd}).json()
    
    skills_count = requests.get(
        API_URL + '/count_skills', params={'limit': 10,
                                           'query': jd}).json()
    
    counts = requests.get(API_URL + '/counts',
                          {'query': jd}).json()

    # Numerical KPIs
    no_jd = str(counts['Number of avaialable jobs'])
    st.markdown(''' ### Number of available jobs:''')
    st.write(no_jd)

    no_comp = str(counts['Number of companies hiring'])
    st.markdown('''### Number of companies hiring:''')
    st.write(no_comp)

    # Altair Charts: breakdown by...

    # companies
    st.markdown('''### Top 30 available jobs by company:''')
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
    if counts['Number of avaialable jobs'] == 0:
        st.write("Sorry, we don't have this job description in our database and can't provide hiring companies")
    else: 
        c_top_comp = get_top_comp()
        st.write(c_top_comp)

    # most in demand skills from the dictionary
    st.markdown('''### Most in demand skills:''')

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
    
    if counts['Number of avaialable jobs'] == 0:
        st.write("Sorry, we don't have this job description in our database and can't provide matching skills")
    else: 
        c_skills_count = get_skill_count()
        st.write(c_skills_count)
