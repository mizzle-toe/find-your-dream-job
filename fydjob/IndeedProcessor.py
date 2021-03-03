#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 12:28:16 2021

@author: vlud
"""

import os
from datetime import date
import pandas as pd
import fydjob.utils as utils
from fydjob.utils import tokenize_text_field
import joblib

class IndeedProcessor:
    
    def __init__(self, data_folder=None):
        self.df_output = None
        if data_folder:
            self.data_folder = data_folder
        else:
            self.data_folder = os.path.join('raw_data', 'indeed_scrapes')
            
        self.filepaths = [os.path.join(self.data_folder, file)
                          for file in os.listdir(self.data_folder)]
        print(f'Loaded files {self.filepaths}')
        
        self.export_folder = os.path.join('raw_data', 'indeed_proc') 
        if not os.path.exists(self.export_folder):
            os.mkdir(self.export_folder)
    
    def pipe(self):
        print('Preprocessing...')
        df = pd.DataFrame()
        
        for filepath in self.filepaths:
            sel = pd.read_json(filepath)
            filename = os.path.split(filepath)[-1]
            sel['query_text'] = ' '.join(filename.split('_')[:2])
            df = df.append(sel)
            
        df.reset_index(inplace=True, drop=True)
        df.drop_duplicates('job_text', inplace=True)
        
        df['location'] = df.location.apply(utils.keep_letters)
        df['tag_language'] = df['job_text'].apply(utils.tag_language)
        
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
    ip = IndeedProcessor(os.path.join('raw_data', 'indeed_scrapes'))
    ip.pipe()
    ip.export()


if __name__ == "__main__":
    main()