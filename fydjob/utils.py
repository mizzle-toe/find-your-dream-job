#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 12:38:33 2021

@author: vlud
"""

from collections import Counter
import fydjob
import os
import json
import string
from langdetect import detect
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np
import pandas as pd

home_path = os.path.dirname(fydjob.__file__)

def join_strings(text):
    return ' '.join(text)

def keep_letters(word):
    '''Removes all chars that are not letters.'''
    return ''.join([char for char in word
                   if char.isalpha()])

def clean_text(text):
    '''Keeps only letter characters (designed for the location field).'''
    return ' '.join([keep_letters(word) for word in text.split(' ')])

def remove_newline(text):
    '''Replaces \n characters with a space.'''
    return ' '.join(text.split('\n'))

def remove_punctuation(text):
    '''Remove punctuation from the text.'''
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')
    return text

def tag_language(text):
    '''Returns language of the text.'''
    ln = detect(text)
    return ln

def remove_stopwords_string(text):
    '''Remove basic stopwords on string text.'''
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    text = [w for w in word_tokens if not w in stop_words]
    return text

def remove_stopwords_list(tokens):
    '''Remove basic stopwords on list of tokens.'''
    stop_words = set(stopwords.words('english'))
    text = [token for token in tokens if not token in stop_words]
    return text

def lemmatize_words(text):
    '''Lemmatize words.'''
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(word) for word in text]
    return lemmatized

def tokenize_text_field(series, to_lowercase=True):
    '''Tokenizes a text field, with or without capital letters.'''
    #transform nan to string to avoid failure mode
    series = series.replace(np.nan, '')
    series = series.apply(remove_punctuation)\
                   .str.strip()\
                   .apply(remove_newline)\
                   .apply(clean_text)

    if to_lowercase:
        series = series.str.lower()

    series = series.apply(word_tokenize)
    return series

def tokenize_text(string):
    return [word.lower() for word in word_tokenize(string)]

def get_unique_tokens(text_field):
    '''Returns set of unique tokens from a tokenized text field.'''
    return set([token
                for tlist in text_field
                for token in tlist])

def split_url(url):
    '''Splits an URL into base URL (String) and parameters(dict).'''
    base, params_str = url.split('?')
    params_str =[str_.split('=') for str_ in params_str.split('&')]
    params = {el[0]: el[1] for el in params_str}
    return base, params

def compose_url(base, params):
    '''Build URL from base (String) and params (dict).'''
    params_strings = []
    for key, val in params.items():
        params_strings.append(f"{key}={val}")
    params_string = '&'.join(params_strings)
    return base + '?' + params_string

def save_skills():
    '''Converts Excel skills file into JSON.'''
    path = os.path.join(home_path, 'data', 'dicts', 'skills_dict.xlsx')
    json_path = os.path.join(home_path, 'data', 'dicts', 'skills_dict.json')

    skill_names = ['business', 'knowledge', 'programming',
                   'soft_skills', 'tech_adjectives']

    skill_names = ['business', 'knowledge', 'programming',
                   'soft_skills']

    skills = {skill: None for skill in skill_names}
    for sheet in range(4):
        l = list(pd.read_excel(path, sheet_name=sheet).iloc[:, 0])
        skills[skill_names[sheet]] = l
    with open(json_path, 'w') as file:
        json.dump(skills, file)
    print(f"Skills dictionary saved at {json_path}.")


def load_skills(remove_duplicates=True):

    '''Loads skills from JSON file.'''
    json_path = os.path.join(home_path, 'data', 'dicts', 'skills_dict.json')
    if not os.path.exists(json_path):
        print("Warning. JSON file not found. Run save_skills first.")
        return
    with open(json_path) as file:
        skills = json.load(file)

    if remove_duplicates:
        flat = []
        for cat, vals in skills.items():
            for val in vals:
                flat.append((cat, val))
        flat = list(set(flat))
        skills_unique = {cat: [] for cat in skills}
        for cat, skill in flat:
            skills_unique[cat].append(skill)
        skills = skills_unique
    return skills

def question_marks(size, before = [], after =[]):
    '''Returns a sequence of question marks fit for inserting values into SQLITE.
    It is possible to append elements before and after.
    '''
    lst = [str(x) for x in before] + ['?']*size + [str(x) for x in after]
    return ','.join(lst)


def category_tagger(series):
        '''
        This function assigns the respective category to the recommended list
        '''
        with open(os.path.join(home_path,"data","dicts","skills_dict.json")) as json_file:
            dictionary= json.load(json_file)

            business_dict = dictionary["business"]
            knowledge_dict = dictionary["knowledge"]
            programming_dict = dictionary["programming"]
            soft_skills_dict = dictionary["soft_skills"]

        try:
            tagged_series = []
            for i in series:
                if i in business_dict:
                    tagged_series.append((i,"business"))
                if i in knowledge_dict:
                    tagged_series.append((i,"knowledge"))
                if i in programming_dict:
                    tagged_series.append((i,"programming"))
                if i in soft_skills_dict:
                    tagged_series.append((i,"soft_skills"))

            return tagged_series
        except:
            return "Sorry,somthing went wrong"

def get_similarities(text, text_vector, keep_perfect=True):
    '''Returns a list of similarity scores between a text and all texts in a text vector.
    Similarity a value between 0 and 1 that shows the proportion of shared unique
    tokens between the texts.
    If keep_perfect is false, it will not return perfect similarities of 1.
    '''
    similarities = []
    for i, t in enumerate(text_vector):
        #try/except to catch division by zero
        try:
            sim = len(set(text) & set(t)) / (len(set(text)) + len(set(t))) * 2
        except:
            sim = 0
        similarities.append((i, sim))
    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    return similarities

def get_skill_category(skill):
    '''Return the category of a skill'''
    skills = load_skills()
    for cat, lst in skills.items():
        if skill in lst:
            return cat

def extract_skills(tokenized_text):
    '''Get the skills mentioned in a tokenized text.'''
    skills = load_skills()
    all_skills = [skill
                  for lst in skills.values()
                  for skill in lst]
    
    return [(token, get_skill_category(token)) 
            for token in tokenized_text
            if token in all_skills]

def count_skills(skills_field):
    '''Returns a count of the skills in the skills column.
    The skills column was built with the extract_skills method.
    Output is in the same for as the skills dictionary 
    returned by load_skills().
    '''
    result = {key: [] for key in load_skills().keys()}
    skills = Counter([skill[0]
                      for lst in skills_field
                      for skill in lst])
    for skill, count in skills.items():
        cat = get_skill_category(skill)
        result[cat].append((skill, count))
    return result