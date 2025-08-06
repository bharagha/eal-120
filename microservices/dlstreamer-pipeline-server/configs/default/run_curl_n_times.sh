#!/bin/bash

# Check if an argument is given
if [ -z "$1" ]; then
  echo "Usage: $0 <number_of_times>"
  exit 1
fi

COUNT=$1

for ((i=1; i<=COUNT; i++)); do
  echo "Request #$i"
  curl -s -o /dev/null -w "Status: %{http_code}\n" \
    localhost:8080/pipelines/user_defined_pipelines/unequal_fps_pipeline \
    -X POST -H 'Content-Type: application/json' -d '{}'
done
