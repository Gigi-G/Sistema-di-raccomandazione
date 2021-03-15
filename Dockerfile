FROM python:alpine

RUN apk add poppler-dev pkgconfig libxslt-dev g++ gcc
RUN pip3 install lxml pdftotext

COPY . /home/Recommender_System

WORKDIR /home/Recommender_System

ENTRYPOINT ["python3"]