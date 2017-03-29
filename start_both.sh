#!/bin/bash -e
trap "exit" INT
while /bin/true; do
    python utility.py -e
done &
echo "started utility starting api_server"
python api_server.py
echo "started api_server"
