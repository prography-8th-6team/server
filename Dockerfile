# /server/Dockerfile
FROM python:3.10

RUN apt-get -y update
RUN apt-get -y install vim

RUN mkdir /server
ADD . /server

WORKDIR /server

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN python3 manage.py makemigrations --settings=config.settings.develop
RUN python3 manage.py migrate --settings=config.settings.develop
RUN python3 manage.py collectstatic  --noinput --settings=config.settings.develop

EXPOSE 8001
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "config.wsgi.develop:application"]