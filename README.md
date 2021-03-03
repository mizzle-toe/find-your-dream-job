# Indeed Scraper

Scrapes job offers from Indeed.com. To use it, download `chromedriver` from the Google Drive folders and place it in `drivers/`. 

Supports Indeed API parameters. When not specified, the default parameters are:

```python
start = 0 #the job offer at which to start
filter = 1 #the API tries to filter out duplicate postings
sort = 'date' #get the newest job offers (alternative is 'relevant')
```

To run the scraper:

```bash
pip install -r requirements.txt
python -m find-your-dream-job.IndeedScraper
```

Input job title, location, and a limit on the job offers to extract. 

Output is saved in `raw_data/indeed_scrapes/`. Filename format is `jobtitle_location_date_limit`. 

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

Functionnal test with a script:

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
