FROM python:3.9
RUN export DEBIAN_FRONTEND=noninteractive

# Create Virtual Environment

RUN apt-get update && apt-get -y upgrade

RUN yes | pip install --upgrade pip

COPY /covid_app/requirements.txt ./requirements.txt
COPY . .
# Make build script exectuable
# TODO rename build.sh to deploy.sh

RUN yes | pip install --upgrade pip
EXPOSE 8080 
RUN yes | pip install -r ./requirements.txt
RUN chmod +x /covid_app/covidApp.py
WORKDIR /covid_app
CMD gunicorn -b 127.0.0.1:80 covidApp:my_server
