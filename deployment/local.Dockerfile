FROM python:3.10-slim-bullseye
WORKDIR /app  
RUN pip install --no-cache-dir poetry==1.4.2
COPY . .
RUN poetry install
RUN apt-get update && apt-get install build-essential -y