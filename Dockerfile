# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM ubuntu:latest

# set environment variables
#   prevents python writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
#   prevents python buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Install gmsh and dependencies
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get install -y python3.10
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-gmsh

# Install Python dependencies
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src /src

WORKDIR /src