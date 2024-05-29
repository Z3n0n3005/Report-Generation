from python:3.10

WORKDIR /code

COPY ./hf-requirements.txt .
RUN pip --cache-dir ./tmp/pipcache install -r hf-requirements.txt

COPY ./worker-requirements.txt .
RUN pip --cache-dir ./tmp/pipcache install -r worker-requirements.txt