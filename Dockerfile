FROM python:3.8.3

ENV PYTHONUNBUFFERED=1
RUN mkdir /project
WORKDIR /project
COPY requirements.txt /project/
RUN pip install -r requirements.txt
COPY . /project/

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
