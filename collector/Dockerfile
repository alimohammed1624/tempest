FROM python:3.11-alpine

ENV PYTHONPATH /usr/lib/python3.11/site-packages

EXPOSE 8002
COPY ./requirements.txt ./
RUN pip install -r ./requirements.txt
COPY . /src
WORKDIR /src
ENTRYPOINT ["./entrypoint.sh"]