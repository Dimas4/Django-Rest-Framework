FROM python:3.6

COPY init.sql /docker-entrypoint-initdb.d/10-init.sql
COPY requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app
