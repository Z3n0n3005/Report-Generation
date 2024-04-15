FROM python:3.10-alpine
# Install dependencies
WORKDIR /code/lib

# Set the grobid-python-client
RUN apk update &&\
    apk add git &&\
    apk add --no-cache gcc musl-dev linux-headers &&\
    git clone https://github.com/kermitt2/grobid_client_python

WORKDIR /code
# Set Flask env
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000
COPY . .
RUN pip install -r requirement.txt
CMD ["ash", "/code/run.sh"]