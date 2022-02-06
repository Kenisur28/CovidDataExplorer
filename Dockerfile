FROM python:3.9
RUN export DEBIAN_FRONTEND=noninteractive

# Create Virtual Environment

RUN apt-get update && apt-get -y upgrade

#RUN apt-get -y install apache2
#RUN apt-get -y install apache2-dev


RUN yes | pip install --upgrade pip
EXPOSE 8080 

COPY . ./app

RUN yes | pip install -r ./app/covid_app/requirements.txt


CMD gunicorn -b 127.0.0.1:80 ./app/covid_app/wsgi
