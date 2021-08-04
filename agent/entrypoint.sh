#!/bin/sh

# waiting for the API to be up and running then start the agent
bash /app/wait-for -t 60 api:8080/api -- python /app/app.py
