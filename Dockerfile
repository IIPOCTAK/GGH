FROM python:3.7

WORKDIR /code

COPY . /code

RUN cp matrix_cache.json /tmp

RUN pip3 install colored accessify numpy