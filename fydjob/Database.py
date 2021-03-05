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
        self.data_path = os.path.join(home_path, 'output', 'indeed_proc', 'processed_data.joblib')
        
    def create_tables(self):
        '''Creates main table to store job postings.'''
        
        conn = sqlite3.connect(self.db_path)
        
        conn.execute('''
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
            conn.execute(f'''
                          CREATE TABLE IF NOT EXISTS {col}
                          (id integer PRIMARY KEY,
                           job_id INTEGER NOT NULL,
                           list_index INTEGER,
                           token TEXT,
                           FOREIGN KEY(job_id) REFERENCES jobads(job_id)
                           )
                          ''')
        
        conn.commit()
        conn.close()
                          
    def reset_all(self):
        '''Deletes the database and creates it again. Data and schema will be lost.'''
        os.remove(self.db_path)
        
    def populate(self, limit=None):
        '''Populates the database. 
        WARNING: We are currently not uploading offers which are not tagged as English!
        '''
        
        conn = sqlite3.connect(self.db_path)
        
        print("Populating database.")
        df = joblib.load(self.data_path)
        print("Loaded data from", self.data_path)
        
        if limit:
            df = df[:limit]
        
        df = df[df.tag_language == 'en']
        cur = conn.cursor()
        
        for i, row in df.iterrows():
            print(i)
            #check if text is already in db
            #sanitize quotation marks to avoid errors!
            #add percentage at the end for SQL wildcard
            text = row['job_text'].replace('"', '')[:300] + "%"
            
            try:
                query = cur.execute(f'SELECT * FROM jobads WHERE job_text LIKE "{text}"').fetchall()
                if query:
                    print('Job offer already in database. Skipping.')
                    continue
            except:
                print("Failed to check for duplicates in database. Will add anyway.")
                pass
            
            basic_vals = row[columns]
            token_vals = row[token_columns]
            
            last_id = cur.execute('SELECT MAX(job_id) FROM jobads').fetchone()[0]
            if not last_id : last_id = 0
            new_id = last_id + 1
            
            vals = [new_id] + list(basic_vals)
            q_marks = f"({'?,'*len(vals)}"[:-1] + ')'
            sql = "INSERT INTO jobads VALUES" + q_marks
            
            try:
                cur.execute(sql, vals)
            except:
                print("Failed to add job at index" + str(i))
                continue
            
            for col in token_columns:
                tokens = row[col]
                for list_index, token in enumerate(tokens):
                    vals = [new_id, list_index, token]
                    sql = f"INSERT INTO {col} VALUES (NULL, ?, ?, ?)"
                    cur.execute(sql, vals)
        
        conn.commit()
        conn.close()
        print("Done populating database!")
        
    def to_frame(self):
        '''Loads the database as a Pandas dataframe.'''
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        df = pd.read_sql_query("SELECT * FROM jobads", conn)
        
        '''
        
        for col in token_columns:
            df[col] = None
        
        for i, row in df.iterrows():
            job_id = row['job_id']
            for col in token_columns:
                #get the tokens rows from SQL
                sql = f"SELECT * FROM {col} WHERE job_id={job_id}"
                result = cur.execute(sql).fetchall()
                if result:
                    #sort by third column, which is the tokens list index
                    result = sorted(result, key=lambda x: x[2])
                    #extract tokens and insert them in dataframe
                    tokens = [x[3] for x in result]
                    df.at[i, col] = tokens
                    
        '''
        conn.close()
        return df
    
    def export_csv(self, path):
        '''Exports the database as CSV.'''
        self.to_frame().to_csv(path)
                   
        
#df_path = os.path.join(home_path, 'output', 'indeed_proc', 'processed_data.joblib')
#df = joblib.load(df_path)
#db = Database()
#db.reset_all()
#db.create_tables()
#db.populate()
#cur = db.conn.cursor()