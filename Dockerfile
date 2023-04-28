FROM python:3.7

WORKDIR /code

COPY . /code

RUN mv matrix_cache.json /tmp

RUN pip3 install colored accessify numpy

CMD python3 main.py test_message
