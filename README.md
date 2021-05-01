# How to run locally

Clone the repository in a new folder, create a new virtual environment and install the package. 

```bash
git clone https://github.com/mizzle-toe/find-your-dream-job.git
cd find-your-dream-job
pyenv virtualenv fydjob-local
pyenv activate fydjob-local
pip install .
```

Start the Docker service and run:

```
docker run -e PORT=8000 -p 4050:8000 vladeng/find-your-dream-job:final
```

Finally:

```
streamlit run fydjob/FindYourDreamJob.py
```

If you can't run Streamlit, try deleting the `.streamlit` folder in your home directory.

---

# Install model

Install package in development mode: 

```bash
pip install -e .
```

Package name is `fydjob`. Example:

```python
import fydjob.utils as utils 
from fydjob.utils import tokenize_text_field
```

# How to get the data locally (final version)

1. Pull master and merge with your branch.
2. Download jobs.db from `Google_Drive/database`.
3. Place the file in `find-your-dream-job/fydjob/database`.
4. `cd` in the main folder `find-your-dream-job`
5. `python short-pipeline-run`

To load the data:

```python
from fydjob.NLPFrame import NLPFrame
df = NLPFrame().df
```

# Pipeline

The **long pipeline** (which will be supported by our package) works like this: 

1.  `IndeedScraper`. Scrape jobs from Indeed.
2. `IndeedProcessor`. Load scraped jobs and Kaggle data. Integrate, remove job offers with identical text, and export as a dataframe.
3. `Database`. Populate the SQLLite database. Ensure not to add duplicates. 
4. `Database`. Do a whole pass through the database, removing duplicates according to our set similarity measure (long process, up to 30 minutes). 
5. `NLPFrame`. Export database to dataframe (`ndf`), add NLP processing columns (such as tokenized fields). 
6. Apply NLP algorithms to dataframe, export results. 

The **short pipeline** will start with stages 5-6. We will deploy our current database to the backend and stages 5-6 will be done on the server. 

Upon scraping new job offers, they should be processed, inserted into the database, and a new similarity sweep should be executed. 

# Indeed Scraper

Scrapes job offers. To use it, download `chromedriver` from the Google Drive folders and place it in `drivers/`. 

Supports Indeed API parameters. When not specified, the default parameters are:

```python
start = 0 #the job offer at which to start
filter = 1 #the API tries to filter out duplicate postings
sort = 'date' #get the newest job offers (alternative is 'relevant')
```

To run the scraper:

```bash
pip install -r requirements.txt
python -m fydjob.IndeedScraper
```

Input job title, location, and a limit on the job offers to extract. 

Output is saved in `fydjob/output/indeed_scrapes/`. Filename format is `jobtitle_location_date_limit`. 

# Preprocessor

Loads JSON files from `fydjob/output/indeed_scrapes` and Kaggle file from `fydjob/output/kaggle`. Joins the dataframes and applies basic preprocessing. To run as a script:

```bash
python -m fydjob.IndeedProcessor 
```

To run as a class: 

``` python
from fydjob.IndeedProcessor import IndeedProcessor
ip = IndeedProcessor()
```

Output is saved in `fydjob/output/indeed_proc`

# Skills dictionary

The skills dictionary is assembled [here](https://docs.google.com/spreadsheets/d/1McSTyy1-kRt-B_Vs8Z-S7OEDVPgWSPwWpCHGnY8AKP0/edit?usp=sharing). The file spreadsheet is downloaded as Excel file and placed into `fydjob/data/dicts/skills_dict.xlsx`. Then:

```python
from fydjob import utils
utils.save_skills()     #extracts skills and saves them in JSON
utils.load_skills()     #loads the skills from JSON file
```

This is just the setup. If you haven't changed the pipeline, just run `utils.load_skills` to get the skills.
