FROM python:3.6

RUN python3.6 -m venv env3

RUN mkdir /usr/src/shiptalent_backend

WORKDIR /usr/src/shiptalent_frontend

COPY . .

RUN yum install zlib1g-dev libjpeg-dev
RUN python3.6 -m venv env3
RUN source env3/bin/activate
RUN pip install -r requirements.txt
RUN pip install preview-generator
RUN ./manage.py collectstatic
RUN ./manage.py makemigrations
RUN ./manage.py migrate
RUN ./manage.py runserver 0.0.0.0:8000

EXPOSE 8000

CMD ["python", "manage.py", "0.0.0.0:8000"]