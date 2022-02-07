
"""gunicorn WSGI server configuration."""
from multiprocessing import cpu_count
from os import environ



bind = '0.0.0.0:' + environ.get('PORT', '8080')
