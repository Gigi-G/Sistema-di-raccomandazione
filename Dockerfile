#FROM python:alpine
#
#RUN apk add poppler-dev pkgconfig libxslt-dev g++ gcc
#RUN pip3 install lxml pdftotext beautifulsoup4 pandas python-telegram-bot
#RUN pip3 install ruamel.yaml
#RUN pip3 install sklearn
#
#COPY . /home/Recommender_System
#
#WORKDIR /home/Recommender_System
#
#ENTRYPOINT ["python3"]
FROM python:3.8

COPY . /home/Recommender_System

WORKDIR /home/Recommender_System

RUN apt-get update -y \
    && apt-get install build-essential libpoppler-cpp-dev pkg-config python3-dev -y
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]