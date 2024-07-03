FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

RUN pip install pipenv

COPY . .

WORKDIR /app/src


CMD [ "pipenv", "run", "run_and_start"]
