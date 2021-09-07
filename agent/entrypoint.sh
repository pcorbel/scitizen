#!/bin/bash

# waiting for the API to be up and running then start the agent
/app/wait-for -t 60 localhost:8080/api -- python /app/app.py
