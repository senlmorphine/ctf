FROM ghcr.io/downunderctf/docker-vendor/nsjail:ubuntu-18.04

COPY /challenge/challenge.py /home/ctf/chal/pwn
COPY /challenge/wordlist.txt /home/ctf/chal/wordlist.txt

RUN chmod +x /home/ctf/chal/pwn

ENV TIME_LIMIT 30
