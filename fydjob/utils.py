#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 12:38:33 2021

@author: vlud
"""

import string
from langdetect import detect
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np


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

def remove_stopwords(text):
    '''Remove basic stopwords.'''
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(text) 
    text = [w for w in word_tokens if not w in stop_words] 
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