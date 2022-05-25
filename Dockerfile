FROM ubuntu:focal

RUN apt update; apt -y install build-essential curl
ADD stadyn.cpp Makefile /opt/

WORKDIR /opt/
RUN make
