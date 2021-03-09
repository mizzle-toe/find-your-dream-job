#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 16:41:31 2021

@author: vlud
"""
import os
import sqlite3
import fydjob
import numpy as np
import pandas as pd
import joblib
from fydjob.utils import question_marks

home_path = os.path.dirname(fydjob.__file__) 

class Database:
    '''Manages connection to SQLITE db.'''
    
    def __init__(self):
    
        folder = os.path.join(home_path, 'database')
        
        if not os.path.exists(folder):
            print('Creating database at', folder)
            os.mkdir(folder)
        
        self.db_path = os.path.join(folder, 'jobs.db')
        self.data_path = os.path.join(home_path, 'output', 'indeed_proc', 'processed_data.joblib') 
        
    def print_paths(self):
        print('os.getcwd()\n', os.getcwd())
        print('os.path.dirname(fydjob.__file__)\n', os.path.dirname(fydjob.__file__))
        
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
         
        conn.commit()
        conn.close()
                          
    def reset_all(self):
        '''Deletes the database and creates it again. Data and schema will be lost.'''
        if os.path.exists(self.db_path):    
            os.remove(self.db_path)
        else:
            print("No DB found.")
        
    def populate(self, limit=None):
        '''Populates the database. 
        WARNING: We are currently not uploading offers which are not tagged as English!
        '''
        
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        print("Populating database.")
        df = joblib.load(self.data_path)
        print("Loaded data from", self.data_path)
        
        if limit:
            df = df[:limit]
        
        df = df[df.tag_language == 'en']
        
        for i, row in df.iterrows():
            #reorder row! some columns seem to be scrambled in the db
            row = row[list(df.columns)].replace(np.nan, 'NULL')
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
            
            last_id = cur.execute('SELECT MAX(job_id) FROM jobads').fetchone()[0]
            if not last_id : last_id = 0
            new_id = last_id + 1
            
            vals = [new_id] + list(row)
            #q_marks = f"({'?,'*len(vals)}"[:-1] + ')'
            q_marks = question_marks(len(vals))
            sql = f'''INSERT INTO jobads(job_id, job_title, job_text, 
                                        company, location, job_info,
                                        query_text, source, job_link,
                                        tag_language, reviews)
                      VALUES ({q_marks})
                      '''
            try:
                cur.execute(sql, vals)
            except:
                print("Failed to add job at index" + str(i))
                continue
        conn.commit()
        conn.close()
        print("Done populating database!")
        
    def to_frame(self):
        '''Loads the database as a Pandas dataframe.'''
        conn = sqlite3.connect(self.db_path)
        print(f"Loading database from {self.db_path} as dataframe.")
        df = pd.read_sql_query("SELECT * FROM jobads", conn)
        conn.close()
        return df
    
    def export_csv(self, path):
        '''Exports the database as CSV.'''
        self.to_frame().to_csv(path) 
        
    def remove_sims_duplicates(self):
        print('Removing duplicates on similarity measure...')
        sdi_path = os.path.join(home_path, 'output', 'sims_duplicates_ids.joblib') 
        if not os.path.exists(sdi_path):
            print('Sims duplicates file not found. Skipping.')
            return
        
        job_ids_to_remove = joblib.load(sdi_path)
        conn = sqlite3.connect(self.db_path) 
        cur = conn.cursor() 
            
        for id_ in job_ids_to_remove:
            sql = '''DELETE FROM jobads WHERE job_id=?'''
            cur.execute(sql, [id_])
            print('Deleted id', id_)
        
        print("Similarity sweep completed")
        conn.close()