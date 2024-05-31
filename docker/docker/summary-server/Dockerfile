FROM python:3.10

WORKDIR /code
# Set Flask env
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

# For caching torch
COPY ./hf-requirements.txt .
RUN pip --cache-dir ./tmp/pipcache install -r hf-requirements.txt

COPY ./summary-server-requirements.txt .
RUN pip --cache-dir ./tmp/pipcache install -r summary-server-requirements.txt

COPY . .

CMD ["flask", "run", "--debug"]