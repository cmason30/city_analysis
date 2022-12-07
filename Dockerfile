FROM public.ecr.aws/lambda/python:3.9

#RUN apk update && apk upgrade && \
#    apk add --no-cache bash git openssh

#RUN mkdir /app
#WORKDIR /app

RUN pip install praw

COPY scraperfiles . ${LAMBDA_TASK_ROOT}
#RUN cd ../ & COPY ../data .

CMD ["python", "-u", "conv_scraper.py"]



