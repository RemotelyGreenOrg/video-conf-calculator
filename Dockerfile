# syntax=docker/dockerfile:1
FROM python:3.9-alpine
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
RUN pytest
ENTRYPOINT [ "python", "-m", "vc_calculator" ]
