FROM python:3.8.6-buster

COPY . find-your-dream-job/
COPY requirements.txt requirements.txt

RUN mkdir find-your-dream-job/fydjob/output
RUN pip install -r requirements.txt
RUN pip install -e find-your-dream-job/.

RUN short-pipeline-run
CMD uvicorn fydjob.api:app --host 0.0.0.0 --port $PORT
