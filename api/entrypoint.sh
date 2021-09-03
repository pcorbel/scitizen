#!/bin/sh

# start the API server
uvicorn --host 0.0.0.0 --port 8080 --timeout-keep-alive 120 --log-level warning app:app
