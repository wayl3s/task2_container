FROM debian:latest

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y zip
RUN apt-get clean

COPY ./archive.py .

RUN chmod +x archive.py

ENTRYPOINT ["python3", "archive.py"]