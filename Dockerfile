# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim-buster

# set environment variables
#   prevents python writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
#   prevents python buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Install opencascade build dependencies
RUN apt-get update
RUN apt-get install -y software-properties-common

RUN apt-get install -y libocct-foundation-dev
RUN apt-get install -y git

RUN git clone http://gitlab.onelab.info/gmsh/gmsh.git

RUN apt-get install -y cmake gcc g++

WORKDIR gmsh
RUN mkdir build
WORKDIR build
RUN cmake ..
RUN make

# Install Python dependencies and Gunicorn
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src /src

WORKDIR /src