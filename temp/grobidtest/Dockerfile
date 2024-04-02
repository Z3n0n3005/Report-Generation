FROM python:3.10-alpine
# Install dependencies
WORKDIR /src/lib
RUN apk update &&\
    apk add git &&\
    git clone https://github.com/kermitt2/grobid_client_python

WORKDIR /src
EXPOSE 8080
COPY . .
RUN pip install -r requirement.txt
CMD ["./run.sh"]