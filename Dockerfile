FROM python:3.8.6-buster

COPY . find-your-dream-job/
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN pip install find-your-dream-job/.

#RUN short-pipeline-run
#CMD uvicorn fydjob.api:app --host 0.0.0.0 --port $PORT
