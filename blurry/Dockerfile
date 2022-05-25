FROM ubuntu:22.04

EXPOSE 1337

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y update && \
    apt-get -y install socat coreutils libssl-dev gcc python3

RUN mkdir /chall
COPY chall/this_is_the_real_flag.txt /
COPY chall/wrapper.py /
COPY chall/blur.c /chall/

RUN gcc /chall/blur.c -o /blurry -lcrypto -s && \
    chmod 555 /blurry && \
    chmod 444 /this_is_the_real_flag.txt 

RUN rm /chall/blur.c 

WORKDIR /
CMD socat -T 30 \
    TCP-LISTEN:1337,nodelay,reuseaddr,fork \
    EXEC:"stdbuf -i0 -o0 -e0 /usr/bin/python3 /wrapper.py"
