FROM python:3.9

# Create Virtual Environment

RUN apt update
RUN apt install apache2
RUN apt install apache2-dev


RUN pip install --upgrade pip

COPY requirements.txt ./app/requirements.txt
COPY . ./app/
WORKDIR ./app/

RUN pip install --upgrade pip
EXPOSE 8080 
COPY requirements.txt /app/requirements.txt
RUN python -m pip install -r requirements.txt


CMD gunicorn -b 127.0.0.1:80 wsgi

