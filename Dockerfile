FROM python:3.9
MAINTAINER dziugas.tornau@gmail.com

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create and set work directory
RUN mkdir /management
WORKDIR /management

# copy and install dependencies
COPY ./requirements.txt /management/requirements.txt
RUN pip install -r requirements.txt
