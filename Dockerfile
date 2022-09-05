# Use the official ubuntu image
FROM ubuntu:latest

# Install gmsh and dependencies
RUN apt-get update -y
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get install -y python3.10
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-gmsh

# Manually install some packages
RUN pip install dash_vtk
RUN pip install pytest

# Install Python dependencies
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src /src

WORKDIR /src