FROM python:3.8

COPY . /home/Recommender_System

WORKDIR /home/Recommender_System

RUN apt-get update -y \
    && apt-get install build-essential libpoppler-cpp-dev pkg-config python3-dev -y
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]