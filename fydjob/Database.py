#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 16:41:31 2021

@author: vlud
"""
import os
import sqlite3
import fydjob
import pandas as pd
import joblib
from fydjob.utils import question_marks

home_path = os.path.dirname(fydjob.__file__)

columns = ['job_title', 'job_text',	'company', 'location',	
           'job_info', 'job_link', 'query_text', 'source',	
           'tag_language', 'reviews']

token_columns = ['job_info_tokenized', 'job_text_tokenized', 
               'job_text_tokenized_titlecase', 'job_title_tokenized']

class Database:
    '''Manages connection to SQLITE db.'''
    def __init__(self):
        
        folder = os.path.join(home_path, 'database')
        
        if not os.path.exists(folder):
            os.mkdir(folder)
        
        self.db_path = os.path.join(folder, 'jobs.db')
        self.conn = sqlite3.connect(self.db_path)
        self.data_path = os.path.join(home_path, 'output', 'indeed_proc', 'processed_data.joblib')
        
    def create_tables(self):
        '''Creates main table to store job postings.'''
        self.conn.execute('''
                          CREATE TABLE IF NOT EXISTS jobads
                          (job_id INTEGER UNIQUE PRIMARY KEY,
                           job_title TEXT,
                           job_text TEXT,
                           company TEXT,
                           location TEXT,
                           job_info TEXT,
                           job_link TEXT,
                           query_text TEXT,
                           source TEXT,
                           tag_language TEXT,
                           reviews TEXT
                           )
                          ''')
         
        for col in token_columns:
            self.conn.execute(f'''
                          CREATE TABLE IF NOT EXISTS {col}
                          (id integer PRIMARY KEY,
                           job_id INTEGER NOT NULL,
                           list_index INTEGER,
                           token TEXT,
                           FOREIGN KEY(job_id) REFERENCES jobads(job_id)
                           )
                          ''')
        
        self.conn.commit()
                          
    def reset_all(self):
        '''Deletes the database and creates it again. Data and schema will be lost.'''
        os.remove(self.db_path)
        self.conn = sqlite3.connect(self.db_path)
        
    def populate(self):
        df = joblib.load(self.data_path)[:10]
        cur = self.conn.cursor()
        
        for i, row in df.iterrows():
            
            basic_vals = row[columns]
            token_vals = row[token_columns]
            
            last_id = c.execute('SELECT last_insert_rowid()').fetchone()[0]
            new_id = last_id + 1
            
            vals = [new_id] + list(basic_vals)
            q_marks = f"({'?,'*len(vals)}"[:-1] + ')'
            sql = "INSERT INTO jobads VALUES" + q_marks
            cur.execute(sql, vals)
            
            for col in token_columns:
                tokens = row[col]
                for list_index, token in enumerate(tokens):
                    vals = [new_id, list_index, token]
                    sql = f"INSERT INTO {col} VALUES (NULL, ?, ?, ?)"
                    cur.execute(sql, vals)
        
        self.conn.commit()
                   
df_path = os.path.join(home_path, 'output', 'indeed_proc', 'processed_data.joblib')
df = joblib.load(df_path)

db = Database()
db.reset_all()
db.create_tables()
c = db.conn.cursor()

'''
def main():
    db = Database()

if __name__ == "__main__":
    main() 
'''