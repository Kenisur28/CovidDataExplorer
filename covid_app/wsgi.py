#!/usr/bin/env python
from covidApp import my_app as app


application = app.server
application.run(host="127.0.0.1", port=8080)
    
