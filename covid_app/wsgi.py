#!/usr/bin/env python
from covidApp.covidApp import my_app as app



if __name__ == "__main__":
    application = app.server
    application.run(host="127.0.0.1", port=8080)
    
