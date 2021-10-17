FROM python:3.8.8-slim-buster
ENV PYTHONUNBUFFERED=1
# RUN mkdir /app 
WORKDIR /app/backend/
ADD ./requirements.txt .
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y gcc libpq-dev && \
    pip3 install -r /app/backend/requirements.txt --no-cache-dir &&\
    apt-get clean
COPY . .