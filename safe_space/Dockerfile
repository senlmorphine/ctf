FROM python:3

RUN apt-get -y update && \
    apt-get -y install socat coreutils

EXPOSE 1337

COPY src/flag.txt /
COPY src/findme.py /

RUN chmod 555 /findme.py && \
    chmod 444 /flag.txt

CMD socat -T 30 \
    TCP-LISTEN:1337,nodelay,reuseaddr,fork \
    EXEC:"python3 findme.py"