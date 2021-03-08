FROM python:3.8.6-buster

WORKDIR /fydjob

COPY . .

RUN pip install .

RUN short-pipeline-run

CMD uvicorn fydjob.api:app --host 0.0.0.0 --port $PORT
