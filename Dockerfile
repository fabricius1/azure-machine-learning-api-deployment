FROM ubuntu:20.04

ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y --no-install-recommends build-essential r-base python3.10 python3-pip
ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY django_code .env ./
CMD python3 manage.py runserver 0.0.0.0:80
