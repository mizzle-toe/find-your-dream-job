#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 12:28:16 2021

@author: vlud
"""
import fydjob
import os
from datetime import date
import pandas as pd
import fydjob.utils as utils
from fydjob.utils import tokenize_text_field
import joblib

home_path = os.path.dirname(fydjob.__file__)

class IndeedProcessor:
    '''Process Indeed job posting files and output one dataframe.'''
    def __init__(self):
        self.df_output = None
        self.data_folder = os.path.join(home_path, 'output', 'indeed_scrapes')
        self.kaggle_folder = os.path.join(home_path, 'output', 'kaggle')
        
        self.filepaths = [os.path.join(self.data_folder, file)
                          for file in os.listdir(self.data_folder)]
        print(f'Loaded files in {self.data_folder}.')
        
        self.export_folder = os.path.join(home_path, 'output', 'indeed_proc')
        
        if not os.path.exists(self.export_folder):
            try:
                os.mkdir(self.export_folder)
            except:
                print(f"Warning. Can't create folder {self.export_folder}.")
                
        if not os.path.exists(self.kaggle_folder):
            try:
                os.mkdir(self.kaggle_folder)
            except:
                print("Warning. Coud not create folder {self.kaggle_folder}.")
                
    def get_jsons(self):
        '''Retrieves JSON files and returns them in the form of dataframes.'''
        frames = []
        for filepath in self.filepaths:
            if filepath.endswith('.json'):
                sel = pd.read_json(filepath)
                filename = os.path.split(filepath)[-1]
                sel['query_text'] = ' '.join(filename.split('_')[:2])
                sel['source'] = 'scrape_json'
                frames.append(sel)
                print(f'Loaded {filepath}')
        return frames
    
    def get_kaggle1(self, filename='data_scientist_job_market_in_the_us.csv'):
        '''Retrieves Kaggle dataframe and homologates the data.'''
        path = os.path.join(self.kaggle_folder, filename)
        print(f"Loaded {path}")
        sel = pd.read_csv(path)
        sel['source'] = 'kaggle_1'
        
        cols = {'position': 'job_title',
                'description': 'job_text'
                }
        
        sel = sel.rename(columns=cols)
        return sel
        
    
    def pipe(self):
        '''Load JSON files from scraper and Kaggle dataset. 
        Assemble into a single dataframe and export as joblib.
        '''
        print('Preprocessing...')
        df = pd.DataFrame()
        
        frames = self.get_jsons()
        kaggle = self.get_kaggle1()
        
        for frame in frames:
            df = df.append(frame)
        
        df = df[df.job_text.notna()]

        #we apply tag language to the scrapings only
        df['tag_language'] = df['job_text'].apply(utils.tag_language)
        
        #append kaggle
        df = df.append(kaggle)
        df = df[df.job_text.notna()]
            
        df.reset_index(inplace=True, drop=True)
        df.drop_duplicates('job_text', inplace=True)
        df = df[df.job_text.notna()]
        
        df['location'] = df.location.apply(utils.keep_letters)
        
        df['job_info_tokenized'] = tokenize_text_field(df['job_info'])
        df['job_text_tokenized'] = tokenize_text_field(df['job_text'])
        df['job_text_tokenized_titlecase'] = tokenize_text_field(df['job_text'], to_lowercase=False)
        df['job_title_tokenized'] = tokenize_text_field(df['job_title']) 

        self.df_output = df
        print('Preprocessing completed.')
        
    def export(self):
        today_str = date.today().isoformat()
        filename = f"ip_{today_str}.joblib"
        export_path = os.path.join(self.export_folder, filename)
        joblib.dump(self.df_output, export_path)
        print(f'Saved dataframe at {export_path}.')
   
def main():    
    ip = IndeedProcessor()
    ip.pipe()
    ip.export()

if __name__ == "__main__":
    main()