#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 09:42:02 2021

@author: vlud

Indeed API parameters

Filter: If set1 to 0, returns all job offers.


"""
import fydjob
import os
from time import sleep
import urllib.parse
from selenium import webdriver
import json
import random
from datetime import date 
from fydjob.utils import split_url, compose_url

home_path = os.path.dirname(fydjob.__file__)

class IndeedScraper:
    def __init__(self):
        self.base = "https://de.indeed.com/jobs"
        self.chrome_driver_path = os.path.join(home_path, 'drivers', 'chromedriver')
        self.output_path = os.path.join(home_path, 'output', 'indeed_scrapes')
        
        if not os.path.exists(os.path.join(home_path, 'output')):
            try:
                os.mkdir(os.path.join(home_path, 'output'))
            except:
                print("Warning. Creation of 'output' directory failed.")

        if not os.path.exists(self.output_path):
            try:
                os.mkdir(self.output_path)
            except:
                print(f"Warning. Creation of {self.output_path} failed.")
            
        self.driver = None
        self.jobs_elements = []
    
    def _get_url(self,
                job_title, 
                location, 
                params = None):
    
        '''Returns an Indeed URL with for a given job title and location.
        It is possible to add more parameters to the query through kwargs
        '''
        
        query_params = {
            'q': '+'.join(job_title.split(' ')),
            'l': location,
            }
        
        #set default values for api parameters
        #these are passed only if they are absent in the params argument
        #filter=1 removes duplicate jobs
        
        default_vals = {'start': 0,
                        'filter': 1,
                        'sort': 'date'}
        
        for param, val in default_vals.items():
            if params and param not in params:
                params[param] = val
            if not params:
                params = {param: val}
        
        query_params = {**query_params, **params}
 
        params_str = urllib.parse.urlencode(query_params, safe='+')
        url = self.base + '?' + params_str
        return url
    
    def _accept_cookies(self):
        self.driver.find_element_by_id('onetrust-accept-btn-handler').click()
    
    def start_chrome_driver(self):
        self.driver = webdriver.Chrome(self.chrome_driver_path)
        print('Started Chrome driver.')
        
    def _change_page(self, value=None, back=False):
        '''Changes page by setting start to defined value or adding ten to current value.'''
        this_url = self.driver.current_url
        base, params = split_url(this_url)
        
        if value: 
            params['start'] = value
        else:
            if 'start' not in params:
                print("Error.'Start' value not defined and URL does not have start parameter.")
                return
            delta = (-10 if back else 10)
            params['start'] = int(params['start']) + delta
        
        new_url = compose_url(base, params) 
        print('Changing page')   
        self.driver.get(new_url)
        
    def _kill_popover(self):
        '''If a popover element has appeared, it kills it.'''
        try:
            popover = self.driver.find_element_by_id('popover-foreground')
            popover.find_element_by_id('popover-x').click()
        except:
            pass
        
    def get_job_attributes(self, job_div):
        try:
            job_title = job_div.find_element_by_id('vjs-jobtitle').text
        except:
            job_title = None
        try:
            job_text = job_div.find_element_by_id('vjs-content').text
        except:
            job_text = None
        try:
            company = job_div.find_element_by_id('vjs-cn').text
        except:
            company= None
        try:
            location = job_div.find_element_by_id('vjs-loc').text
        except:
            location = None
        try:
            job_info = job_div.find_element_by_id('vjs-jobinfo').text
        except:
            job_info = None
        try:
            job_link = self.driver.current_url
        except:
            job_link = None
            
        return {'job_title': job_title,
                'job_text': job_text,
                'company': company,
                'location': location,
                'job_info': job_info,
                'job_link': job_link}
        
    def _get_jobs_webelements(self):
        '''Extracts jobs webelements from current page.
        and saves them as HTML. 
        '''
        jobs = []
         
        job_clickers = self.driver.find_elements_by_class_name('jobtitle')
        print("Extracting jobs...")
        for i, je in enumerate(job_clickers):
            try:
                idle = random.choice(range(2, 11))
                sleep(idle)
                je.click()
                sleep(10)
                #after the click, indeed will sometimes open a new tab!
                print(self.driver.current_url)
                if self.base not in self.driver.current_url.lower():
                    print("Opened a new tab! Trying to go back...")
                    self.driver.back()
                job_div = self.driver.find_element_by_id('vjs-container')            
                job = self.get_job_attributes(job_div)
                #print(job)
                jobs.append(job)
            except:
                print('Could not get job.')
        return jobs
    
    def save_jobs(self, path):
        with open(path, 'w') as file:
            json.dump(self.jobs_elements, file)
            print(f'Saved jobs at {path}')
            
    def load_jobs(self, path):
        try:
            with open(path) as file:
                self.jobs_elements = json.load(file)
                print(f"Loaded jobs from {path}.")
        except:
            print('Did not find jobs to load.')
            return
        
    def job_search(self,
                   job_title,
                   location,
                   limit=None,
                   filename=None,
                   api_params=None):
        
        if not filename:
            snake = lambda x: x.replace(' ', '_')
            filename = f"{snake(job_title)}_{snake(location)}_{date.today().isoformat()}_{limit}.json"
            
        save_path = os.path.join(self.output_path, filename)
        
        self.load_jobs(save_path)
        
        url = self._get_url(job_title, location, api_params)
        print(f'Starting search at {url}')
        self.driver.get(url)
        sleep(3)
        self._accept_cookies()
        n_found = int(\
                      self.driver.find_element_by_id('searchCountPages')\
                          .text\
                          .split(' ')[-2]\
                          .replace('.', ''))
        
        print(f"{n_found} jobs listed.")
        
        #initial "start" value for page. will increase by 10 at every page shift
        start_value = 0
        #waiting params - onset and long wait time. simulate humanoid coffee breaks
        wait_counter = 0
        long_wait_onset = random.choice(range(50, 100))
        long_wait_time = random.choice(range(120, 600))
        
        while True:
            this_url = self.driver.current_url
            wait_counter += 1
            if wait_counter == long_wait_onset:
                print(f"Coffee time! Sleeping for {long_wait_time} seconds.")
                sleep(long_wait_time)
                long_wait_onset = random.choice(range(50, 100))
                long_wait_time = random.choice(range(120, 600))
                wait_counter = 0
                
            sleep(3)
            self._kill_popover()
            
            try:
                new_jobs = self._get_jobs_webelements()
                if new_jobs:
                    self.jobs_elements += new_jobs
                else:
                     #we did not retrieve new jobs!
                     #we might be lost. return to previous url
                     print("No jobs retrieved. Attempting to revert URL.")
                     self.driver.get(this_url)
            except:
                print('Error. Could not continue with job extraction.')
                break
            
            if limit:
                if len(self.jobs_elements) >= limit:
                    break
            
            print(len(self.jobs_elements))
            self.save_jobs(save_path)
            start_value += 10
            
            try:
                self._change_page(value=start_value)
            except:
                print("Error. Could not switch page.")
                break
            
            sleep(10)
            self._kill_popover()
        
        self.save_jobs(save_path)
        print('Job search done!')
        
def main():
    title = input('job title: ')
    location = input('location: ')
    limit = input('Job offers to extract (skip for no limit): ')
    if not limit: limit = None
    scraper = IndeedScraper()
    scraper.start_chrome_driver() 
    scraper.job_search(title, location, limit=int(limit))

if __name__ == "__main__":
    main()