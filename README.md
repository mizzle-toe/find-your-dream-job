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



---

### Boilerplate below

---



# Data analysis

- Document here the project: find-your-dream-job
- Description: Project Description
- Data Source:
- Type of analysis:

Please document the project the better you can.

# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for find-your-dream-job in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/find-your-dream-job`
- Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "find-your-dream-job"
git remote add origin git@github.com:{group}/find-your-dream-job.git
git push -u origin master
git push -u origin --tags
```

Functional test with a script:

```bash
cd
mkdir tmp
cd tmp
find-your-dream-job-run
```

# Install

Go to `https://github.com/{group}/find-your-dream-job` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/find-your-dream-job.git
cd find-your-dream-job
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
find-your-dream-job-run
```
