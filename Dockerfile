FROM python:3.6
ENV PYTHONUNBUFFERED 1  

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev bash \
    apk add zlib1g-dev libjpeg-dev

RUN mkdir /config  
ADD /config/requirements.txt /config/  
RUN pip install -r /config/requirements.txt
RUN mkdir /src
WORKDIR /src