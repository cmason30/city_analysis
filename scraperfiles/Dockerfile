FROM python:3.9-alpine

RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh

RUN mkdir /app
WORKDIR /app

RUN pip install praw

COPY . .
RUN cd ../ & COPY ../datafiles .

CMD ["python", "-u", "conv_scraper.py"]



