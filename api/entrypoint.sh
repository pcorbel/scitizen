#!/bin/sh

# waiting for postgresql to be up and running then start the api
bash /app/wait-for -t 60 database:5432 -- gunicorn --bind 0.0.0.0:8080 --timeout 120 wsgi:app
