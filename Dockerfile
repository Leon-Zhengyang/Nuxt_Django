FROM python:3.9.1-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN apk add --no-cache build-base mariadb-connector-c-dev --virtual .pynacl_deps python3-dev py3-setuptools build-base freetype-dev libffi-dev jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/