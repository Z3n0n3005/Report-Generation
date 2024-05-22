FROM python:3.10
# FROM petronetto/pytorch-alpine
# Install dependencies
# WORKDIR /code/lib

# COPY ./lib .
# Set the grobid-python-client
# RUN echo "|--> Update" &&\
#     apk update &&\
#     apk add git &&\
#     apk add --no-cache gcc musl-dev linux-headers &&\
#     git clone https://github.com/kermitt2/grobid_client_python
    

WORKDIR /code
# Set Flask env
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

copy ./requirement.txt .
RUN pip --cache-dir ./tmp/pipcache install -r requirement.txt

COPY . .

# RUN pip install --upgrade pip
# CMD ["ash", "/code/run.sh"] 
CMD ["flask", "run", "--debug"]