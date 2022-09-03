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
WORKDIR ../../
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the codebase into the image
# COPY . ./

# # Remove static files since these should be served by nginx server
# RUN rm -rf assets
# RUN rm -rf static

# RUN apt-get install -y libtool autoconf automake gfortran gdebi
# # RUN apt-get install -y gcc-multilib libxi-dev libxmu-dev libxmu-headers
# RUN apt-get install -y libxi-dev libxmu-dev libxmu-headers
# RUN apt-get install -y libx11-dev mesa-common-dev libglu1-mesa-dev
# RUN apt-get install -y libfontconfig1-dev
# RUN apt-get install -y libfreetype6 libfreetype6-dev
# RUN apt-get install -y tcl tcl-dev tk tk-dev

# # Download opencascade source
# RUN curl -L -o occt.tgz "http://git.dev.opencascade.org/gitweb/?p=occt.git;a=snapshot;h=refs/tags/V7_3_0;sf=tgz"
# RUN tar zxf occt.tgz
# WORKDIR occt-V7_3_0
# RUN mkdir build
# WORKDIR build
# RUN apt-get install -y cmake
# RUN cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_MODULE_Draw=0 -DBUILD_MODULE_Visualization=0 -DBUILD_MODULE_ApplicationFramework=0 ..
# # # Notes:
# # # * if you installed dependencies (e.g. Freetype) in non-standard locations, add the option -DCMAKE_PREFIX_PATH=path-of-installed-dependencies
# # # * if you don't have root access, add -DCMAKE_INSTALL_PREFIX=path-to-install
# # # * to build static libraries, add -DBUILD_LIBRARY_TYPE=Static
# RUN make
# RUN make install
