
FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN mkdir /pharmacy

WORKDIR /pharmacy

ADD . /pharmacy/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt