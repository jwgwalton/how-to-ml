#!/bin/bash

uvicorn --reload \
  --log-level=debug \
  --workers ${WORKERS:-2} \
  --timeout-keep-alive 10800 \
  --host 0.0.0.0 \
  --port 8080 \
  'app.server:app'
