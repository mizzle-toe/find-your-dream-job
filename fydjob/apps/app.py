# import streamlit as st
# import altair as alt
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import joblib
# from fydjob import utils
# from gensim.models import Word2Vec
# from fydjob.NLPFrame import NLPFrame
# import requests

# # get data from
# #api
# #url = 'http://0.0.0.0:3000'
# #response = requests.get(url)
# #response.json()

# #local data
# data = NLPFrame().df
# #data = joblib.load('/Users/jasminkazi/code/mizzle-toe/find-your-dream-job/fydjob/output/indeed_proc/processed_data.joblib')
# data = data.drop(columns=['job_info_tokenized','job_text_tokenized_titlecase', 'job_title_tokenized','job_text_tokenized'])
# data = data.sample(n=2000)


# #Sidebar
# # Title
# st.sidebar.markdown("""
#     # Find your Dream Job
#     ## Please enter the following in order to collect all relevant job offers and analyze the requirements
# """)

# # store Input in variable
# jd = st.sidebar.text_input('Job Description', 'Data Scientist')
# # use a regular expression for filtering the df, as Data Scientist (m/w/x) would be filtered out
# regex_jd = '^'+jd
# city = st.sidebar.text_input('City', 'Berlin')
# comp = st.sidebar.text_input('Company')
# # use a regular expression for filtering the df, as Data Scientist (m/w/x) would be filtered out
# regex_comp = '^'+comp
# #Button: if button is clicked, jump to next page and show exploratory view
# if st.sidebar.button('Analyze'):
#     # filter data based on job input
#     data = data.loc[data.job_title.str.contains(regex_jd)]  
#     # filter data based on city input  only if we get the city

#     # filter data based on job input
#     data = data.loc[data.job_title.str.contains(regex_comp)]
# # switch between pages by using Radio Button
# #st.sidebar.radio('View Page', ['Overview','Job Offers'])

# # Numerical KPIs
# no_jd = str(data['job_title'].count())
# st.markdown("""
# ### Number of available jobs:""")
# st.write(no_jd)

# no_comp = str(data['company'].nunique())
# st.markdown("""
# ### Number of companies hiring:""")
# st.write(no_comp)


# # Altair Charts: breakdown by...
# #job description
# st.markdown("""
# ### Distribution of Job Titles:""")

# @st.cache(allow_output_mutation=True)
# def get_jobtitles():

#     source_job = pd.DataFrame(data['query_text'].value_counts().reset_index())
#     source_job= source_job.rename(columns = {'index':'Job', 'query_text':'Count'})
    
#     c_jd= alt.Chart(source_job).mark_bar().encode(
#     x='Count',
#     y='Job'
#     )
#     text = c_jd.mark_text(
#     align='left',
#     baseline='middle',
#     dx=3  # Nudges text to right so it doesn't appear on top of the bar
#     ).encode(
#         text='Count:Q'
#     )

#     return c_jd+text

# c_jd = get_jobtitles()
# st.write(c_jd)

# #languages
# st.markdown("""
# ### Available jobs broken down by posting language:""")

# @st.cache(allow_output_mutation=True)
# def get_languages():
#     source_lang = pd.DataFrame(data['tag_language'].value_counts()).reset_index()
#     source_lang = source_lang.rename(columns = {'index':'Posting Language', 'tag_language':'Count'})
#     c_language = alt.Chart(source_lang).transform_joinaggregate(
#         Total='sum(Count)',
#     ).transform_calculate(
#         Percentage="datum.Count / datum.Total"
#     ).mark_bar().encode(
#         alt.X('Percentage:Q', axis=alt.Axis(format='.0%')),
#         y='Posting Language:N'
#     )
#     return c_language
# c_lang = get_languages()
# st.write(c_lang)

# #companies
# st.markdown("""
# ### Top 30 available jobs by company:""")

# @st.cache(allow_output_mutation=True)
# def get_top_comp():
#     #df
#     source_comp = pd.DataFrame(data['company'].value_counts().reset_index())
#     source_comp= source_comp.rename(columns = {'index':'Company', 'company':'Count'})
#     source_comp = source_comp.nlargest(30, 'Count')
#     #barchart
#     bars = alt.Chart(source_comp).mark_bar().encode(
#         x='Count:Q',
#         y=alt.Y('Company:N', sort='-x')
#     )
#     # text on bars
#     text = bars.mark_text(
#         align='left',
#         baseline='middle',
#         dx=3  # Nudges text to right so it doesn't appear on top of the bar
#     ).encode(
#         text='Count:Q'
#     )

#     c_top_comp = (bars + text).properties(height=500)
#     return c_top_comp
# #call companies
# c_top_comp = get_top_comp()
# st.write(c_top_comp)

# #skills
# st.markdown("""
# ### Most in demand skills:""")
# # get the aggregated values for the skills in all JDs
# @st.cache(allow_output_mutation=True)
# def get_skill_aggr(all_vacancies):
#     categories = utils.load_skills()
#     vacancy_set = set(all_vacancies)
#     matching_skill_per_category = {}

#     for category in categories:
#         matching_skill_per_category[str(category)]=vacancy_set.intersection(categories[category])
    
#     occ = {}
#     for category in categories:
#         occ[category] = {}
#         for s in matching_skill_per_category[str(category)]:
#             occ[category][s] =  all_vacancies.count(s)
#     return occ

# #create the skill set for all jobs and count the occurences
# all_vacancies=[]
# for job in data['job_text_tokenized_processed']:
#     #print(len(job))
#     all_vacancies = all_vacancies + job
# total_occurences = get_skill_aggr(all_vacancies)


# # put the result into a data frame
# df = pd.DataFrame(total_occurences).reset_index()
# df= df.rename(columns = {'index':'skill'})
# #transform the dataframes -> put the skill category in one column
# df_bus = df[['skill','business']].dropna().sort_values('business', ascending = False).rename(columns = {'business':'count'})
# df_bus['category']='business'
# df_know = df[['skill','knowledge']].dropna().sort_values('knowledge', ascending = False).rename(columns = {'knowledge':'count'})
# df_know['category']='knowledge'
# df_code = df[['skill','programming']].dropna().sort_values('programming', ascending = False).rename(columns = {'programming':'count'})
# df_code['category']='programming'
# df_soft = df[['skill','soft_skills']].dropna().sort_values('soft_skills', ascending = False).rename(columns = {'soft_skills':'count'})
# df_soft['category']='soft skills'
# #make all the sub data frames into one new dataframe
# df_categ = df_bus.append(df_know).append(df_code).append(df_soft)


# @st.cache(allow_output_mutation=True)
# def get_skills(df_categ):
#     #source = df_categ
#     source = df_categ.nlargest(50, 'count')
#     categs = np.array(df_categ['category'].unique())
#     category = np.insert(categs, 0, 'all')
#     #Dropdownbox
#     input_dropdown = alt.binding_select(options = category)
#     selection = alt.selection_single(fields = ['category'], bind = input_dropdown, name= 'Skill ')

#     c_skills= alt.Chart(source).mark_bar().encode(
#     x = ('count:Q'),
#     #i tried getting the top N to work here, so we wouldn't have to filter on top n in the source df
#     # y = alt.Y('skill',sort='-x'),
#     #     ).add_selection(selection).transform_window(
#     #         rank='rank(count)',
#     #         sort=[alt.SortField('count', order='descending')]
#     #         ).transform_filter((selection) & (alt.datum.rank < 10))
#     y = alt.Y('skill',sort='-x')).add_selection(selection).transform_filter(selection)
       
#     return c_skills
# c_skills = get_skills(df_categ)
# st.write(c_skills)



# #Detail page
# w2v_model = Word2Vec.load("../fydjob/data/models/w2v_model_baseline.model")
# #search for skill
# st.markdown("""
# ### Find the closest skills for:""")
# skill = st.text_input('Skill','python')
# word = [skill]
# #st.write(skill)
# df_words= pd.DataFrame(w2v_model.wv.most_similar(word), columns=['Similar word', 'distance']) # works with single words
# #table
# st.table(df_words)

# # list of job offers
# st.table(data)
