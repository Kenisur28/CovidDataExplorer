FROM python:3.9
RUN export DEBIAN_FRONTEND=noninteractive

# Create Virtual Environment

RUN apt-get update && apt-get -y upgrade

#RUN apt-get -y install apache2
#RUN apt-get -y install apache2-dev


RUN yes | pip install --upgrade pip

COPY /covid_app/requirements.txt ./requirements.txt
COPY . .
RUN yes | pip install --upgrade pip
EXPOSE 8080 
RUN yes | pip install -r ./requirements.txt


CMD gunicorn -b 127.0.0.1:80 ./covid_app/wsgi
